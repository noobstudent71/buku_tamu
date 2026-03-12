from django.apps import AppConfig


class TamuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tamu'
# Tambahkan baris ini:
    verbose_name = 'Sistem Buku Tamu'