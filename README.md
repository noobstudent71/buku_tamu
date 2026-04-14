# 📋 Buku Tamu Digital — Panduan Menjalankan Program

> Sistem Buku Tamu Digital berbasis **Django** untuk manajemen kunjungan tamu secara real-time.

---

## 📦 Prasyarat (Install Dulu Sebelum Mulai)

Pastikan komputer kamu sudah terinstall:

| Kebutuhan | Versi | Cek dengan |
|---|---|---|
| **Python** | 3.10+ | `python --version` |
| **pip** | bawaan Python | `pip --version` |

> Kalau belum punya Python, download di → [python.org/downloads](https://www.python.org/downloads/)  
> ✅ Centang **"Add Python to PATH"** saat instalasi!

---

## 🚀 Langkah-Langkah Menjalankan Program

### Step 1 — Buka Folder Project di Terminal

Buka **Command Prompt** atau **PowerShell**, lalu arahkan ke folder project:

```bash
cd C:\bukutamudigital
```

> 💡 Tips: Di Windows Explorer, klik kanan di dalam folder project → pilih **"Open in Terminal"** atau **"Open PowerShell window here"**.

---

### Step 2 — Buat Virtual Environment (Wajib!)

Virtual environment itu seperti "kotak isolasi" agar library project ini tidak campur dengan Python di komputer.

```bash
# Buat virtual environment dengan nama "env"
python -m venv env
```

Setelah dibuat, **aktifkan** dulu:

```bash
# Windows (Command Prompt / PowerShell)
env\Scripts\activate

# Mac / Linux
source env/bin/activate
```

> ✅ Tanda berhasil: di terminal akan muncul tulisan `(env)` di depan prompt.  
> Contoh: `(env) C:\bukutamudigital>`

---

### Step 3 — Install Semua Library yang Dibutuhkan

```bash
pip install django pillow crispy-bootstrap5 django-import-export openpyxl
```

Penjelasan setiap library:

| Library | Fungsi |
|---|---|
| `django` | Framework utama web |
| `pillow` | Untuk kompresi & proses foto KTP / selfie |
| `crispy-bootstrap5` | Form yang tampil lebih cantik dengan Bootstrap 5 |
| `django-import-export` | Fitur export data di Admin |
| `openpyxl` | Generate file laporan Excel (.xlsx) |

---

### Step 4 — Siapkan Database

Jalankan perintah ini untuk membuat tabel-tabel di database (SQLite):

```bash
python manage.py migrate
```

> ✅ Kalau berhasil, akan muncul banyak baris `OK` di terminal.

---

### Step 5 — Buat Akun Admin (Superuser)

Akun ini untuk login ke halaman `/admin/` dan juga login sebagai **KANTOR** (akses penuh).

```bash
python manage.py createsuperuser
```

Nanti akan diminta mengisi:
- **Username** → bebas, misal: `admin`
- **Email** → boleh dikosongkan (tekan Enter)
- **Password** → masukkan password (minimal 8 karakter), **tidak akan terlihat saat diketik**, itu normal!

---

### Step 6 — Jalankan Server! 🎉

```bash
python manage.py runserver
```

Kalau berhasil, terminal akan menampilkan:

```
System check identified no issues (0 silenced).
April 10, 2026 - 07:30:00
Django version 4.2, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Buka browser dan akses → **http://127.0.0.1:8000/**

---

## 🗺️ Peta Halaman (URL) Program

| URL | Halaman | Akses |
|---|---|---|
| `http://127.0.0.1:8000/` | Form Pendaftaran Tamu | Publik (Tamu) |
| `http://127.0.0.1:8000/login/` | Halaman Login | Semua User |
| `http://127.0.0.1:8000/daftar-tamu/` | Dashboard Monitor Tamu | Login (Satpam) |
| `http://127.0.0.1:8000/analytics/` | Dashboard Grafik & Analitik | Login (Kantor) |
| `http://127.0.0.1:8000/arsip-tamu/` | Arsip Semua Data Tamu | Login |
| `http://127.0.0.1:8000/laporan/` | Download Laporan Excel | Login |
| `http://127.0.0.1:8000/admin/` | Panel Admin Django | Superuser |

---

## 👥 Sistem Role / Grup Pengguna

Program ini memiliki **3 jenis pengguna** dengan hak akses berbeda:

| Grup | Setelah Login Diarahkan ke | Fungsi |
|---|---|---|
| **SATPAM** | `/daftar-tamu/` (Monitor tamu) | Melihat & update status tamu |
| **KANTOR** | `/analytics/` (Grafik) | Melihat laporan & analitik |
| **Superuser** | `/analytics/` | Akses penuh semua halaman |

### Cara Tambah User dan Grup via Admin Panel:

1. Buka `http://127.0.0.1:8000/admin/`
2. Login dengan akun superuser yang sudah dibuat
3. Buat **Group** baru → beri nama `SATPAM` atau `KANTOR`
4. Buat **User** baru → assign ke group yang sesuai

---

## 🛠️ Perintah Penting Django (Cheat Sheet)

```bash
# Jalankan server (perintah paling sering dipakai)
python manage.py runserver

# Jalankan di port berbeda (misal port 8080)
python manage.py runserver 8080

# Jalankan agar bisa diakses dari HP di jaringan yang sama
python manage.py runserver 0.0.0.0:8000

# Buat migrasi setelah mengubah models.py
python manage.py makemigrations

# Terapkan migrasi ke database
python manage.py migrate

# Buat akun superuser
python manage.py createsuperuser

# Buka shell interaktif Django (untuk debug)
python manage.py shell
```

---

## ❓ Troubleshooting — Masalah Umum

### ❌ `'python' is not recognized as an internal or external command`
Python belum di-install atau belum ditambahkan ke PATH.  
→ Reinstall Python, centang **"Add to PATH"**.

---

### ❌ `ModuleNotFoundError: No module named 'django'`
Library belum terinstall, atau virtual environment belum aktif.  
→ Aktifkan `env` dulu, lalu `pip install django`.

---

### ❌ `django.db.utils.OperationalError: no such table`
Lupa menjalankan migrate.  
→ Jalankan: `python manage.py migrate`

---

### ❌ `Address already in use` / `Port is already in use`
Port 8000 sedang dipakai proses lain.  
→ Matikan proses lama atau ganti port: `python manage.py runserver 8080`

---

### ❌ Foto tidak bisa diupload / error saat save tamu
Library `Pillow` belum terinstall.  
→ `pip install pillow`

---

## 📁 Struktur Folder Project

```
bukutamudigital/
├── config/              # Konfigurasi utama Django
│   ├── settings.py      # Pengaturan database, installed apps, dll
│   ├── urls.py          # URL routing utama
│   └── wsgi.py
│
├── tamu/                # Aplikasi utama (Django App)
│   ├── models.py        # Struktur database (BukuTamu, PIC, Instansi)
│   ├── views.py         # Logika bisnis & fungsi halaman
│   ├── forms.py         # Form pendaftaran tamu
│   ├── urls.py          # URL routing untuk app tamu
│   ├── admin.py         # Konfigurasi panel admin
│   └── templates/       # File HTML tampilan
│       └── tamu/
│
├── media/               # Foto KTP & Selfie tamu (auto-generated)
│   ├── ktp/
│   └── swafoto/
│
├── db.sqlite3           # Database (auto-generated setelah migrate)
├── manage.py            # ⬅️ File utama untuk menjalankan perintah Django
└── env/                 # Virtual environment (jangan di-commit ke Git)
```

---

## ✅ Checklist Cepat (TL;DR)

Untuk yang mau langsung jalan tanpa baca panjang:

```bash
# 1. Aktifkan virtual environment
env\Scripts\activate

# 2. Install dependencies (cukup sekali)
pip install django pillow crispy-bootstrap5 django-import-export openpyxl

# 3. Siapkan database (cukup sekali)
python manage.py migrate

# 4. Buat admin (cukup sekali)
python manage.py createsuperuser

# 5. JALANKAN! (ini yang dipakai setiap hari)
python manage.py runserver
```

Lalu buka browser: **http://127.0.0.1:8000/**

---

*Dibuat untuk memudahkan setup & operasional Buku Tamu Digital.*
