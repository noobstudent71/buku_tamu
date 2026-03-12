from django import forms
from .models import BukuTamu

class TamuForm(forms.ModelForm):
    class Meta:
        model = BukuTamu
        fields = [
            'nama', 
            'no_hp', 
            'instansi', 
            'no_polisi', 
            'jumlah_tamu',
            'pic_tuju', 
            'keperluan', 
            'foto_ktp', 
            'foto_wajah', 
            'sudah_janji',
            'kategori_tamu',  
            'bawa_barang',    
            'jumlah_barang',
        ]
        
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Nama Lengkap'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xx-xxxx-xxxx', 'type': 'tel'}),
            'instansi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Perusahaan / Company','list': 'list_instansi',}),
            'no_polisi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: N 1234 ABC'}),
            'jumlah_tamu': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'pic_tuju': forms.Select(attrs={'class': 'form-select'}), # Tetap Dropdown
            'keperluan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Tujuan kedatangan...'}),
            'foto_ktp': forms.ClearableFileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*',      # Hanya terima gambar
                'capture': 'environment'  # PAKSA BUKA KAMERA BELAKANG
            }),
            'foto_wajah': forms.ClearableFileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*',      # Hanya terima gambar
                'capture': 'environment'   # PAKSA BUKA KAMERA BELAKANG
            }),
            'sudah_janji': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kategori_tamu': forms.Select(attrs={'class': 'form-select'}),
            'bawa_barang': forms.TextInput(attrs={'class': 'form-control'}),
            'jumlah_barang': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        # Mengganti label agar lebih sopan/jelas di layar
        labels = {
            'pic_tuju': 'Ingin Bertemu Siapa?',
            'foto_ktp': 'Ambil Foto KTP',
            'foto_wajah': 'Ambil Foto Selfie',
            'no_polisi': 'Nomor Polisi (Jika bawa kendaraan)',
        }