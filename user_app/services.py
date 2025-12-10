# user_app/services.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password # Gunakan ini untuk hashing
from .models import UserProfile, FreeSubscription, ListeningHistory, UserPreferences, Notification, PlayEvent
from datetime import datetime
import time

class UserAuthenticator:
    def register(self, request, username, password, display_name):
        if User.objects.filter(username=username).exists():
            print(f"Error: Username '{username}' sudah ada.")
            return None, "Username sudah digunakan."

        print(f"\nMendaftarkan user baru: {username}...")

        # Buat user Django (password otomatis di-hash oleh create_user)
        user = User.objects.create_user(username=username, password=password)

        # Buat profil dan data terkait menggunakan model Django
        profile = UserProfile.objects.create(user=user, display_name=display_name)
        subscription = FreeSubscription.objects.create(user=user)
        history = ListeningHistory.objects.create(user=user)
        preferences = UserPreferences.objects.create(user=user)

        print(f"Registrasi berhasil untuk {display_name}!")
        return user, None # Kembalikan user dan pesan error jika ada

    def login(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"\nLogin berhasil! Selamat datang, {user.profile.display_name}.")
            return user
        else:
            print("\nError: Username atau password salah.")
            return None

    def logout(self, request):
        logout(request)
        print("Logout berhasil. Sesi telah diakhiri.")

# --- SERVIS UNTUK LOGIKA USER ---

class UserService:
    def play_song(self, user, song_object):
        # Asumsi song_object adalah instance dari model Song dari app lain
        print(f"\n{user.profile.display_name} memutar lagu: {song_object.title}")

        # Tambahkan ke history Django
        user.listening_history.add_event(song_object)

        # Cek iklan berdasarkan subscription Django
        if not user.subscription.can_skip_ads():
            print("--- Memutar Iklan (Pengguna Gratis) ---")
            time.sleep(1) # Simulasi waktu iklan

        print(f"🎵 Sedang Memutar: {song_object.title}...")
        time.sleep(2) # Simulasi durasi lagu

    def like_song(self, user, song_object):
        # Logika untuk menyukai lagu, misalnya menambahkan ke ManyToManyField
        # Di sini kita hanya print, karena implementasi ManyToManyField mungkin belum dibuat
        print(f"[User] {user.profile.display_name} menyukai {song_object.title}")

    def follow_user(self, user, user_to_follow):
        # Asumsi 'following' adalah ManyToManyField di model User
        # Di sini kita hanya print
        print(f"[User] {user.profile.display_name} sekarang mengikuti {user_to_follow.profile.display_name}")

    def create_playlist(self, user, name):
        # Asumsi model Playlist ada di app lain (misalnya 'playlists')
        try:
            from playlists.models import Playlist
            new_playlist = Playlist.objects.create(name=name, owner=user)
            print(f"[User] Playlist baru dibuat: {new_playlist.name}")
            return new_playlist
        except ImportError:
            print("Model Playlist tidak ditemukan. Pastikan aplikasi 'playlists' sudah diinstal.")
            return None
        except Exception as e:
            print(f"Gagal membuat playlist: {e}")
            return None

    def upgrade_subscription(self, user):
        from .models import PremiumSubscription
        if isinstance(user.subscription, FreeSubscription):
            # Hapus subscription lama
            user.subscription.delete()
            # Buat yang baru
            premium_sub = PremiumSubscription.objects.create(user=user)
            print("[User] Langganan telah di-upgrade ke Premium!")
        else:
            print("[User] Anda sudah menjadi pengguna Premium.")

    def get_unread_notifications(self, user):
        # Ambil dari model Django
        return user.notifications.filter(is_read=False)

    def update_profile(self, user, new_name=None, new_bio=None):
        # Panggil method update_profile dari model Django
        user.profile.update_profile(new_name=new_name, new_bio=new_bio)

    def update_preferences(self, user, new_theme=None, new_quality=None):
        # Panggil method update_settings dari model Django
        user.preferences.update_settings(theme=new_theme, audio_quality=new_quality)
