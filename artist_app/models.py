from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stage_name or getattr(self.user, "username", "Artist")


class Song(models.Model):
    # basic song / product model
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to="songs/")
    cover_image = models.ImageField(upload_to="song_covers/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    upload_date = models.DateTimeField(auto_now_add=True)

    # engagement & sales counters
    play_count = models.PositiveIntegerField(default=0)
    purchase_count = models.PositiveIntegerField(default=0)

    # optional metadata
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-upload_date"]
        indexes = [
            models.Index(fields=["artist"]),
        ]

    def __str__(self):
        return f"{self.title} — {self.artist.stage_name}"

    def increment_play(self, save=True):
        self.play_count = models.F('play_count') + 1
        if save:
            # use F() then refresh to avoid race conditions in high concurrency
            self.save(update_fields=['play_count'])
            self.refresh_from_db(fields=['play_count'])

    def increment_purchase(self, amount=None, save=True):
        # increase counter and optionally record income elsewhere
        self.purchase_count = models.F('purchase_count') + 1
        if save:
            self.save(update_fields=['purchase_count'])
            self.refresh_from_db(fields=['purchase_count'])


class SongPurchase(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="purchases")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="song_purchases")
    purchase_date = models.DateTimeField(default=timezone.now)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-purchase_date"]

    def __str__(self):
        return f"{self.buyer} bought {self.song.title} for {self.price_paid}"
