from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO 
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys 
import os
from datetime import datetime
from django.utils import timezone 
from django.db import models
from .models import Instansi
from django.http import JsonResponse

def search_perusahaan(request):
    # Tangkap huruf yang diketik tamu (misal: "Ots")
    query = request.GET.get('q', '')
    
    if query:
        # Cari di tabel Instansi, kolom 'nama_standar' yang mengandung huruf ketikan
        # distinct() berguna agar tidak ada nama instansi ganda/kembar yang muncul
        hasil = Instansi.objects.filter(nama_standar__icontains=query).values_list('nama_standar', flat=True).distinct()[:10]
        data = list(hasil)
    else:
        data = []
        
    return JsonResponse(data, safe=False)

# ==========================================
# 1. TABEL MASTER DATA PIC (Karyawan)
# ==========================================
class PIC(models.Model): # Nama kelas jadi lebih singkat
    nama_lengkap = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_lengkap

    class Meta:
        verbose_name = "PIC"
        verbose_name_plural = "Daftar PIC"


# ==========================================
# 2. TABEL MASTER DATA INSTANSI (Untuk Dashboard)
# ==========================================
class Instansi(models.Model): # Nama kelas jadi lebih singkat
    nama_standar = models.CharField(max_length=100, unique=True)
    kata_kunci = models.TextField()

    def __str__(self):
        return self.nama_standar

    class Meta:
        verbose_name = "Instansi"
        verbose_name_plural = "Daftar Instansi"


# ==========================================
# 3. FUNGSI RENAME (Ditaruh DI LUAR Class)
# ==========================================
def rename_file_ktp(instance, filename):
    ext = filename.split('.')[-1]
    today = timezone.localtime(timezone.now()).date()
    tanggal_str = today.strftime("%Y%m%d")

    # Hitung antrian hari ini (Manual Count + 1)
    from .models import BukuTamu 
    jumlah_tamu_hari_ini = BukuTamu.objects.filter(waktu_masuk__date=today).count()
    urutan_baru = jumlah_tamu_hari_ini + 1
    
    # Nama File: 20260209-001_KTP.jpg
    filename_baru = f"{tanggal_str}-{str(urutan_baru).zfill(3)}_KTP.{ext}"
    return os.path.join('ktp',filename_baru)

def rename_file_selfie(instance, filename):
    ext = filename.split('.')[-1]
    today = timezone.localtime(timezone.now()).date()
    tanggal_str = today.strftime("%Y%m%d")

    from .models import BukuTamu 
    jumlah_tamu_hari_ini = BukuTamu.objects.filter(waktu_masuk__date=today).count()
    urutan_baru = jumlah_tamu_hari_ini + 1
    
    # Nama File: 20260209-001_SELFIE.jpg
    filename_baru = f"{tanggal_str}-{str(urutan_baru).zfill(3)}_SELFIE.{ext}"
    return os.path.join('swafoto',filename_baru)


# ==========================================
# 4. MODEL KARYAWAN
# ==========================================
class Karyawan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nama_lengkap = models.CharField(max_length=100)
    divisi = models.CharField(max_length=50)
    jabatan = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nama_lengkap} - {self.divisi}"


# ==========================================
# 5. MODEL BUKU TAMU
# ==========================================
class BukuTamu(models.Model):
    STATUS_CHOICES = [
        ('MENUNGGU', 'Menunggu Konfirmasi'),
        ('MASUK', 'Sedang Bertamu'),
        ('SELESAI', 'Selesai Bertamu'),
        ('KELUAR', 'Sudah Checkout'),
    ]
    KATEGORI_CHOICES = [
        ('rekan_bisnis', 'Lokal Rekan Bisnis'),
        ('pemerintahan', 'Pemerintahan'),
        ('akademisi', 'Akademisi'),
        ('overseas', 'Overseas Guests (Luar Negeri)'),
    ]

    # --- Data Diri Tamu ---
    waktu_masuk = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='MENUNGGU')
    nama = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    instansi = models.CharField(max_length=150, verbose_name="Nama Instansi")
    no_hp = models.CharField(max_length=20, verbose_name="No Telfon/HP", default="-")
    no_polisi = models.CharField(max_length=20, verbose_name="No Polisi Kendaraan", blank=True, null=True)
    
    # [REVISI] Upload To pakai Fungsi, bukan String lagi
    foto_ktp = models.ImageField(
        upload_to=rename_file_ktp,  # <--- PANGGIL FUNGSI
        verbose_name="Foto KTP",
        blank=False, null=False
    )
    
    # --- Tujuan ---
    keperluan = models.TextField(verbose_name="Keperluan")
    pic_tuju = models.ForeignKey('PIC', on_delete=models.SET_NULL, null=True, blank=True)
    jumlah_tamu = models.PositiveBigIntegerField(default=1, verbose_name="Jumlah Orang")
    sudah_janji = models.BooleanField(default=False, verbose_name="Sudah Janji?")

    # [REVISI] Upload To pakai Fungsi
    foto_wajah = models.ImageField(
        upload_to=rename_file_selfie, # <--- PANGGIL FUNGSI
        verbose_name="Foto Wajah (Selfie)", 
        blank=True, null=True
    )
    kategori_tamu = models.CharField(
        max_length=50, 
        choices=KATEGORI_CHOICES, 
        default='rekan_bisnis',
        verbose_name="Kategori Tamu"
    )

    # --- System ---
    waktu_keluar = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # [UBAH/TAMBAHKAN INI] Barang Bawaan (Tipe Teks) & Jumlah
    bawa_barang = models.CharField(max_length=200, blank=True, null=True, verbose_name="Barang Bawaan")
    jumlah_barang = models.IntegerField(default=0, verbose_name="Jumlah Barang")

    # --- PROPERTY NOMOR TIKET (PENGGANTI KOLOM DATABASE) ---
    @property
    def nomor_tiket(self):
        if not self.id:
            return "-"
        tanggal_ini = self.waktu_masuk.date()
        urutan = BukuTamu.objects.filter(waktu_masuk__date=tanggal_ini, id__lte=self.id).count()
        tanggal_str = self.waktu_masuk.strftime('%Y%m%d')
        return f"{tanggal_str}-{str(urutan).zfill(3)}"

    # --- LOGIKA SAVE (Hanya Kompres, Tidak Rename/Generate ID Lagi) ---
    def save(self, *args, **kwargs):
        # HAPUS BARIS GENERATE TIKET DI SINI AGAR TIDAK ERROR
        
        # A. Kompres KTP
        if self.foto_ktp:
            try:
                # Cek jika file baru, lakukan kompresi
                if not self.foto_ktp._committed:
                    print("DEBUG: Mengompres Foto KTP...")
                    self.foto_ktp = self.kompres_gambar(self.foto_ktp)
            except AttributeError:
                pass
        
        # B. Kompres Wajah
        if self.foto_wajah:
            try:
                if not self.foto_wajah._committed:
                    print("DEBUG: Mengompres Foto Wajah...")
                    self.foto_wajah = self.kompres_gambar(self.foto_wajah)
            except AttributeError:
                pass
            
        super().save(*args, **kwargs)

    # --- MESIN KOMPRES GAMBAR (TETAP SAMA) ---
    def kompres_gambar(self, image_field):
        im = Image.open(image_field)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        
        # Resize jadi max 1024px
        im.thumbnail((1024, 1024))
        
        output = BytesIO()
        im.save(output, format='JPEG', quality=70)
        output.seek(0)
        
        # Pakai nama asli file (karena sudah di-rename oleh upload_to)
        return InMemoryUploadedFile(
            output, 'ImageField', image_field.name, 
            'image/jpeg', sys.getsizeof(output), None
        )

    def __str__(self):
        return f"{self.nama} - {self.instansi}"
    
    class Meta:
        ordering = ['-waktu_masuk']
        verbose_name_plural = "Daftar Tamu"

    