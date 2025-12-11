from django.urls import path
from . import views

urlpatterns = [
    # 1. Halaman Utama Aplikasi User
    # Menangani akses ke /accounts/ agar tidak 404
    path('', views.home, name='home'),

    # 2. Autentikasi (Register, Login, Logout)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 3. Fitur User (Profil, Update, Notifikasi)
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('notifications/', views.notifications_view, name='notifications'),

    # 4. Fitur Musik (Placeholder agar tidak error)
    path('play/<int:song_id>/', views.play_song_view, name='play_song'),
    path('like/<int:song_id>/', views.like_song_view, name='like_song'),
]