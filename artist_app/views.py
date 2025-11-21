from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import SongUploadForm, SongEditForm
from .models import Artist, Song, SongPurchase

# Helper: get Artist instance for current user or 404
def get_current_artist_or_404(user):
    try:
        return Artist.objects.get(user=user)
    except Artist.DoesNotExist:
        raise Http404("Artist profile not found. You must be an artist to access this page.")


@login_required

def artist_dashboard(request):
    return HttpResponse("Halaman Dashboard Artis OK")

'''def artist_dashboard(request):
    artist = get_current_artist_or_404(request.user)
    songs = artist.songs.all().select_related("artist")
    # overall stats
    total_plays = songs.aggregate(total=Sum("play_count"))["total"] or 0
    total_purchases = songs.aggregate(total=Sum("purchase_count"))["total"] or 0
    total_income = SongPurchase.objects.filter(song__artist=artist).aggregate(
        total=Sum("price_paid")
    )["total"] or Decimal("0.00")

    context = {
        "artist": artist,
        "songs": songs,
        "total_plays": total_plays,
        "total_purchases": total_purchases,
        "total_income": total_income,
    }
    return render(request, "artists/dashboard.html", context)
'''

@login_required
def upload_song(request):
    artist = get_current_artist_or_404(request.user)

    if request.method == "POST":
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = artist
            song.save()
            messages.success(request, "Song uploaded successfully.")
            return redirect(reverse("artists:dashboard"))
    else:
        form = SongUploadForm()

    return render(request, "artists/upload_song.html", {"form": form, "artist": artist})


@login_required
def edit_song(request, song_id):
    artist = get_current_artist_or_404(request.user)
    song = get_object_or_404(Song, id=song_id, artist=artist)

    if request.method == "POST":
        form = SongEditForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, "Song updated.")
            return redirect(reverse("artists:dashboard"))
    else:
        form = SongEditForm(instance=song)

    return render(request, "artists/edit_song.html", {"form": form, "song": song})


@login_required
def delete_song(request, song_id):
    artist = get_current_artist_or_404(request.user)
    song = get_object_or_404(Song, id=song_id, artist=artist)
    if request.method == "POST":
        song.delete()
        messages.success(request, "Song deleted.")
        return redirect(reverse("artists:dashboard"))
    return render(request, "artists/confirm_delete.html", {"song": song})


def song_list(request):
    """
    Public list of songs (for users to browse).
    """
    songs = Song.objects.select_related("artist").all()
    return render(request, "artists/song_list.html", {"songs": songs})


def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, "artists/song_detail.html", {"song": song})


from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@require_POST
@csrf_exempt
def increment_play_api(request, song_id):
    """
    Simple endpoint for incrementing play_count when user plays a song.
    - Accepts POST (AJAX / fetch).
    - Returns JSON with new play_count.
    NOTE: For production you should protect this (rate-limit, CSRF, auth) to avoid abuse.
    """
    song = get_object_or_404(Song, id=song_id)
    # increment safely
    Song.objects.filter(id=song.id).update(play_count=models.F('play_count') + 1)
    song.refresh_from_db(fields=['play_count'])
    return JsonResponse({"song_id": song.id, "play_count": song.play_count})


# Sales / reporting views (artist-facing)
@login_required
def sales_report(request):
    """
    Returns per-song sales & income.
    """
    artist = get_current_artist_or_404(request.user)
    songs = artist.songs.all()

    report = []
    for song in songs:
        income = SongPurchase.objects.filter(song=song).aggregate(total=Sum("price_paid"))["total"] or Decimal("0.00")
        report.append({
            "song": song,
            "plays": song.play_count,
            "purchases": song.purchase_count,
            "income": income,
        })

    return render(request, "artists/sales_report.html", {"report": report, "artist": artist})
