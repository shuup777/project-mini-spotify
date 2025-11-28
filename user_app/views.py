# user_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .services import UserAuthenticator, UserService
from .models import Notification

def home(request):
    return render(request, 'home.html')

def user_home(request):
    return redirect('profile')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        display_name = request.POST['display_name']
        
        auth_service = UserAuthenticator()
        user, error = auth_service.register(request, username, password, display_name)
        
        if user:
            messages.success(request, 'Akun berhasil dibuat!')
            return redirect('login') # Ganti dengan URL login kamu
        else:
            messages.error(request, error)
    
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        auth_service = UserAuthenticator()
        user = auth_service.login(request, username, password)
        
        if user:
            return redirect('dashboard') # Ganti dengan URL dashboard kamu
        else:
            messages.error(request, 'Username atau password salah.')
    
    return render(request, 'users/login.html')

def logout_view(request):
    auth_service = UserAuthenticator()
    auth_service.logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    unread_notifications = user.notifications.filter(is_read=False).count()
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
def play_song_view(request, song_id):
    # Asumsi model Song ada di app 'music'
    from music.models import Song
    song = get_object_or_404(Song, id=song_id)
    
    service = UserService()
    service.play_song(request.user, song)
    
    return JsonResponse({'status': 'success', 'message': f'{song.title} diputar.'})

@login_required
def like_song_view(request, song_id):
    from music.models import Song
    song = get_object_or_404(Song, id=song_id)
    
    service = UserService()
    service.like_song(request.user, song)
    
    return JsonResponse({'status': 'success'})

@login_required
def notifications_view(request):
    user = request.user
    notifications = user.notifications.all().order_by('-timestamp')
    context = {
        'notifications': notifications
    }
    return render(request, 'users/notifications.html', context)
