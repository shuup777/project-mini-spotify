from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.utils import timezone

# --- Model 1: User Profile (Menyimpan Foto & Bio) ---
class UserProfile(models.Model):
    # Relasi OneToOne: Satu User hanya punya satu Profile
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    # Foto profil akan disimpan di folder 'media/profile_pics'
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)

    def update_profile(self, name=None, bio=None):
        if name: self.display_name = name
        if bio: self.bio = bio
        self.save()

    def __str__(self):
        return self.display_name

# --- Model 2: Subscription (Parent Class untuk Langganan) ---
class Subscription(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='subscription')
    start_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')

    # Helper untuk mendeteksi tipe object (apakah Free atau Premium)
    def get_real_instance(self):
        if hasattr(self, 'freesubscription'): return self.freesubscription
        elif hasattr(self, 'premiumsubscription'): return self.premiumsubscription
        return self

    # Method Polymorphism (akan di-override oleh anak kelas)
    def can_skip_ads(self): return self.get_real_instance()._can_skip_ads()
    def can_download_songs(self): return self.get_real_instance()._can_download_songs()

    # Internal method (default False)
    def _can_skip_ads(self): return False
    def _can_download_songs(self): return False

    def __str__(self):
        return f"Subscription of {self.user.username}"

# --- Model 3: Free Subscription (Anak Kelas) ---
class FreeSubscription(Subscription):
    def _can_skip_ads(self): return False
    def _can_download_songs(self): return False

# --- Model 4: Premium Subscription (Anak Kelas) ---
class PremiumSubscription(Subscription):
    next_billing_date = models.DateTimeField(null=True, blank=True)
    
    def _can_skip_ads(self): return True
    def _can_download_songs(self): return True

# --- Model 5: User Preferences (Pengaturan) ---
class UserPreferences(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='preferences')
    audio_quality = models.CharField(max_length=20, default='Standard') 
    theme = models.CharField(max_length=20, default='Light') 
    enable_explicit_content = models.BooleanField(default=False)

    def update_settings(self, theme=None, quality=None):
        if theme: self.theme = theme
        if quality: self.audio_quality = quality
        self.save()

# --- Model 6 & 7: History & Play Event ---
# Kita butuh model Song dummy agar tidak error jika app lain belum siap
class SongDummy(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    def __str__(self): return self.title

class PlayEvent(models.Model):
    # Mencatat satu kejadian lagu diputar
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=200) 
    timestamp = models.DateTimeField(auto_now_add=True)

class ListeningHistory(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='history')
    play_events = models.ManyToManyField(PlayEvent, blank=True)
    
    def add_event(self, song_title):
        event = PlayEvent.objects.create(user=self.user, song_title=song_title)
        self.play_events.add(event)

# --- Model 8: Notification ---
class Notification(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def mark_as_read(self):
        self.is_read = True
        self.save()