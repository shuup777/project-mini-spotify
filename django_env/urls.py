from django.contrib import admin
from django.urls import path, include # <-- Pastikan include diimpor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_app.urls')), # <-- Tambahkan baris ini
    # Tambahkan URL lain dari aplikasi Anda di sini
    # path('artist/', include('artist_app.urls')),
    # path('payments/', include('payments.urls')),
]
