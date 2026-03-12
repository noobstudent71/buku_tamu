from django.contrib import admin
from django.urls import path, include

# --- TAMBAHAN PENTING (IMPORT) ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tamu.urls')),
]

# --- KODE PEMBUKA JALUR MEDIA ---
# Kode ini artinya: "Jika browser minta alamat file Media, 
# tolong ambilkan file aslinya dari folder MEDIA_ROOT di laptop"
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)