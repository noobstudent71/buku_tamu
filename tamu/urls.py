from django.urls import path
from . import views  # Memanggil views yang ada di satu folder (tamu)

urlpatterns = [
    # Halaman Utama (Form Tamu)
    path('', views.pendaftaran_tamu, name='pendaftaran_tamu'),

    # Halaman Dashboard Satpam
    path('daftar-tamu/', views.daftar_tamu, name='daftar_tamu'),

    # Fungsi Checkout
    path('ubah-status/<int:id>/<str:status_baru>/', views.ubah_status, name='ubah_status'),

    # Fitur Laporan Excel (Yang Baru)
    path('laporan/', views.download_excel, name='laporan_excel'),

    path('arsip-tamu/', views.arsip_tamu, name='arsip_tamu'),

    path('analytics/', views.dashboard_analytics, name='dashboard_analytics'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),
    
    path('api/search-perusahaan/', views.search_perusahaan, name='search-perusahaan'),
    
    path('master-data/', views.master_data, name='master_data'),

    path('master-data/hapus/<str:tipe>/<int:id>/', views.hapus_data, name='hapus_data'),
    
    path('master-data/toggle/<str:tipe>/<int:id>/', views.toggle_status, name='toggle_status'),
]
