from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import PIC, Instansi, BukuTamu
# Kita pakai ImportExportModelAdmin supaya otomatis ada tombol "Export ke Excel"

@admin.register(PIC)
class MasterPICAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'departemen', 'is_active') # Kolom yang tampil di tabel
    list_filter = ('is_active',)                # Filter di samping kanan
    search_fields = ('nama_lengkap',)           # Kotak pencarian

@admin.register(Instansi)
class MasterInstansiAdmin(admin.ModelAdmin):
    list_display = ('nama_standar', 'kata_kunci_singkat')
    search_fields = ('nama_standar', 'kata_kunci')

    # Fungsi pembantu agar tampilan keyword tidak terlalu panjang di tabel
    def kata_kunci_singkat(self, obj):
        if len(obj.kata_kunci) > 50:
            return obj.kata_kunci[:50] + "..."
        return obj.kata_kunci
    kata_kunci_singkat.short_description = 'Daftar Kata Kunci'

@admin.register(BukuTamu)
class BukuTamuAdmin(admin.ModelAdmin):
    # Kita tampilkan nama PIC-nya juga di tabel arsip admin
    list_display = ('nomor_tiket', 'nama', 'instansi', 'get_pic', 'status', 'waktu_masuk')
    list_filter = ('status', 'kategori_tamu')
    search_fields = ('nama', 'instansi', 'nomor_tiket')

    def get_pic(self, obj):
        return obj.pic_tuju.nama_lengkap if obj.pic_tuju else "-"
    get_pic.short_description = 'Bertemu Dengan'