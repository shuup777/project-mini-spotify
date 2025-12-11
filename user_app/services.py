from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Hash password otomatis ditangani oleh create_user, jadi make_password tidak wajib di-import manual di sini
from .models import UserProfile, FreeSubscription, ListeningHistory, UserPreferences, Notification, PremiumSubscription
from django.utils import timezone
from datetime import timedelta

class UserAuthenticator:
    def register(self, request, username, password, display_name):
        if User.objects.filter(username=username).exists():
            return None, "Username sudah digunakan."

        print(f"\nMendaftarkan user baru: {username}...")

        # 1. Buat user Django
        user = User.objects.create_user(username=username, password=password)

        # 2. Buat profil dan data terkait (Sesuai models.py Tahap 2)
        UserProfile.objects.create(user=user, display_name=display_name)
        FreeSubscription.objects.create(user=user)
        ListeningHistory.objects.create(user=user)
        UserPreferences.objects.create(user=user)

        print(f"Registrasi berhasil untuk {display_name}!")
        return user, None

    def login(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Menggunakan try-except untuk menghindari error jika profil belum ada
            try:
                print(f"\nLogin berhasil! Selamat datang, {user.profile.display_name}.")
            except:
                print("\nLogin berhasil (User tanpa profil).")
            return user, "Login Berhasil"
        else:
            print("\nError: Username atau password salah.")
            return None, "Username atau password salah"

    def logout(self, request):
        logout(request)
        print("Logout berhasil.")

# --- SERVIS UNTUK LOGIKA USER ---

class UserService:
    def play_song(self, user, song_object):
        # PERBAIKAN: Menggunakan 'user.history' sesuai related_name di models.py
        try:
            print(f"\n{user.profile.display_name} memutar lagu: {song_object.title}")
            user.history.add_event(song_object.title) # Kita simpan judul lagunya

            # Cek iklan
            if not user.subscription.can_skip_ads():
                print("--- [Iklan] Beli Premium untuk skip iklan ---")
        except Exception as e:
            print(f"Error playing song: {e}")

    def like_song(self, user, song_object):
        print(f"[User] {user.profile.display_name} menyukai {song_object.title}")

    def follow_user(self, user, user_to_follow):
        print(f"[User] {user.profile.display_name} sekarang mengikuti {user_to_follow.profile.display_name}")

    def create_playlist(self, user, name):
        # Kode ini aman, jika app playlists belum ada dia akan return None
        try:
            from playlists.models import Playlist
            new_playlist = Playlist.objects.create(name=name, owner=user)
            return new_playlist
        except ImportError:
            print("Fitur Playlist belum tersedia (App 'playlists' tidak ditemukan).")
            return None
        except Exception as e:
            print(f"Gagal membuat playlist: {e}")
            return None

    def upgrade_subscription(self, user):
        # Cek apakah user saat ini pakai FreeSubscription
        # Kita cek atribut 'freesubscription' (nama model huruf kecil)
        if hasattr(user.subscription, 'freesubscription'):
            old_sub = user.subscription
            old_sub.delete()
            
            # PERBAIKAN: Set tanggal tagihan 30 hari ke depan
            PremiumSubscription.objects.create(
                user=user,
                next_billing_date=timezone.now() + timedelta(days=30)
            )
            print("[User] Langganan telah di-upgrade ke Premium!")
            return True, "Upgrade Berhasil"
        else:
            print("[User] Anda sudah Premium atau status tidak diketahui.")
            return False, "Sudah Premium"

    def get_unread_notifications(self, user):
        return user.notifications.filter(is_read=False)

    def update_profile(self, user, new_name=None, new_bio=None):
        user.profile.update_profile(name=new_name, bio=new_bio)

    def update_preferences(self, user, new_theme=None, new_quality=None):
        user.preferences.update_settings(theme=new_theme, quality=new_quality)