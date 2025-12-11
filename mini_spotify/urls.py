from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # UBAH DI SINI:
    # 1. Hapus baris user_views.home yang lama.
    # 2. Ganti path('user/', ...) menjadi path('', ...).
    # Ini membuat user_app menangani halaman depan (root).
    path('', include('user_app.urls')), 
    
    path('system/', include('system_admin_app.urls')),
    path('artist/', include('artist_app.urls')),
    path('finance/', include('finance.urls')),
]

# Tambahkan ini agar gambar profil bisa muncul saat mode debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)