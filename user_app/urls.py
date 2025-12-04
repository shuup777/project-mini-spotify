from django.urls import path
from .views import (
    register_view, login_view, logout_view, 
    profile_view, update_profile_view,
    notifications_view, play_song_view, like_song_view
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile_view, name='update_profile'),
    path('notifications/', notifications_view, name='notifications'),
    path('play/<int:song_id>/', play_song_view, name='play_song'),
    path('like/<int:song_id>/', like_song_view, name='like_song'),
]
