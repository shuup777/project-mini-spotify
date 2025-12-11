from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .services import UserAuthenticator, UserService
from .models import Notification

# --- HALAMAN UTAMA ---

def home(request):
    return render(request, 'users/home.html')

def user_home(request):
    return render(request, "users/login.html")

# --- AUTHENTICATION ---

def register_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        d_name = request.POST.get('display_name')
        
        auth_service = UserAuthenticator()
        # Method register mengembalikan (user, error_message)
        user, error = auth_service.register(request, u_name, p_word, d_name)
        
        if user:
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('login') 
        else:
            messages.error(request, error)
    
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        
        auth_service = UserAuthenticator()
        # PERBAIKAN: Method login mengembalikan (user, message)
        # Kita harus menangkap keduanya agar tidak error
        user, msg = auth_service.login(request, u_name, p_word)
        
        if user:
            # PERBAIKAN: Redirect ke 'profile' karena 'dashboard' belum ada
            return redirect('profile') 
        else:
            messages.error(request, msg)
    
    return render(request, 'users/login.html')

def logout_view(request):
    auth_service = UserAuthenticator()
    auth_service.logout(request)
    messages.info(request, "Anda telah logout.")
    return redirect('login')

# --- USER FEATURES ---

@login_required
def profile_view(request):
    user = request.user
    # Mengambil notifikasi (pastikan model Notification sudah dimigrasi)
    try:
        unread_notifications = user.notifications.filter(is_read=False).count()
    except:
        unread_notifications = 0
        
    context = {
        'user': user,
        'unread_notifications': unread_notifications
    }
    return render(request, 'users/profile.html', context)

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        new_name = request.POST.get('display_name')
        new_bio = request.POST.get('bio')
        
        service = UserService()
        service.update_profile(request.user, new_name=new_name, new_bio=new_bio)
        messages.success(request, 'Profil berhasil diperbarui.')
    
    return redirect('profile')

@login_required
def notifications_view(request):
    user = request.user
    notifications = user.notifications.all().order_by('-timestamp')
    context = {
        'notifications': notifications
    }
    return render(request, 'users/notifications.html', context)

# --- MUSIC FEATURES (DUMMY SEMENTARA) ---
# Fitur ini akan error jika App Music belum ada.
# Saya tambahkan try-except agar website tetap jalan.

@login_required
def play_song_view(request, song_id):
    try:
        # Mencoba import (akan gagal jika app music belum ada)
        from music.models import Song
        song = get_object_or_404(Song, id=song_id)
        
        service = UserService()
        service.play_song(request.user, song)
        return JsonResponse({'status': 'success', 'message': f'{song.title} diputar.'})
    except ImportError:
        return JsonResponse({'status': 'error', 'message': 'Modul Music belum terinstall.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def like_song_view(request, song_id):
    try:
        from music.models import Song
        song = get_object_or_404(Song, id=song_id)
        
        service = UserService()
        service.like_song(request.user, song)
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'error', 'message': 'Fitur belum tersedia.'})