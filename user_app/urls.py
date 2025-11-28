# user_app/urls.py
from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('play/<int:song_id>/', views.play_song_view, name='play_song'),
    path('like/<int:song_id>/', views.like_song_view, name='like_song'),
    path('', user_home, name='user_home'),
]
