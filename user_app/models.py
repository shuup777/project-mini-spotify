# user_app/models.py
from django.db import models
from django.contrib.auth.models import User # Gunakan User bawaan Django
from django.utils import timezone
from abc import ABC, abstractmethod

# --- MODEL UNTUK PROFIL USER ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    profile_picture_url = models.URLField(default='default_avatar.png', max_length=500)

    def update_profile(self, new_name=None, new_bio=None):
        if new_name:
            self.display_name = new_name
        if new_bio:
            self.bio = new_bio
        self.save()

    def __str__(self):
        return f"{self.display_name} (User: {self.user.username})"


# --- MODEL UNTUK LANGGANAN ---
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    start_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='Active')

    class Meta:
        abstract = True

    @abstractmethod
    def can_skip_ads(self):
        pass

    @abstractmethod
    def can_download_songs(self):
        pass


class FreeSubscription(Subscription):
    def can_skip_ads(self):
        return False

    def can_download_songs(self):
        return False

    def __str__(self):
        return f"Free Subscription for {self.user.username}"


class PremiumSubscription(Subscription):
    next_billing_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.next_billing_date:
            self.next_billing_date = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    def can_skip_ads(self):
        return True

    def can_download_songs(self):
        return True

    def __str__(self):
        return f"Premium Subscription for {self.user.username}"


# --- MODEL UNTUK RIWAYAT PEMUTARAN ---
class PlayEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='play_events')
    song_title = models.CharField(max_length=200) # Atau relasi ke model Song jika ada
    song_artist = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.song_title} oleh {self.song_artist} - {self.timestamp}"


class ListeningHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='listening_history')

    def add_event(self, song_object):
        event = PlayEvent.objects.create(
            user=self.user,
            song_title=song_object.title,
            song_artist=song_object.artist_name
        )
        print(f"[History] Mencatat: {song_object.title}")
        return event

    def get_recently_played(self, count=5):
        return self.user.play_events.all().order_by('-timestamp')[:count]


# --- MODEL UNTUK PREFERENSI USER ---
class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    audio_quality = models.CharField(max_length=20, default='Normal')
    theme = models.CharField(max_length=20, default='Dark')
    enable_explicit_content = models.BooleanField(default=False)

    def update_settings(self, audio_quality=None, theme=None, explicit=None):
        if audio_quality:
            self.audio_quality = audio_quality
        if theme:
            self.theme = theme
        if explicit is not None:
            self.enable_explicit_content = explicit
        self.save()
        print("[Preferences] Setelan diperbarui.")


# --- MODEL UNTUK NOTIFIKASI ---
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    link_target = models.URLField(blank=True, null=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()
        print(f"[Notification] Ditandai sebagai terbaca: {self.message[:30]}...")

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"[{status}] {self.message}"
