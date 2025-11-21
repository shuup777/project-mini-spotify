from django.urls import path
from . import views

app_name = "artist_app"

urlpatterns = [
    path('', views.artist_dashboard, name="dashboard"),
    path("dashboard/", views.artist_dashboard, name="dashboard"),
    path("upload/", views.upload_song, name="upload-song"),
    path("song/<int:song_id>/edit/", views.edit_song, name="edit-song"),
    path("song/<int:song_id>/delete/", views.delete_song, name="delete-song"),
    path("sales-report/", views.sales_report, name="sales-report"),

    # public facing list and detail (optional)
    path("songs/", views.song_list, name="song-list"),
    path("songs/<int:song_id>/", views.song_detail, name="song-detail"),

    # API-like endpoint to increment play count via POST (AJAX)
    path("api/song/<int:song_id>/play/", views.increment_play_api, name="api-increment-play"),
]
