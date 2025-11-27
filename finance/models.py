from django.db import models

# finance/models.py
from django.db import models
from django.contrib.auth.models import User # Mengacu ke sistem User yang diurus oleh tim User
from django.utils import timezone 

# =======================================================
# MODEL 1: SubscriptionPlan (Objek Paket Langganan)
# =======================================================
class SubscriptionPlan(models.Model):
    """Mendefinisikan jenis-jenis paket langganan yang tersedia."""
    name = models.CharField(max_length=50, unique=True, verbose_name="Nama Paket")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Harga (Rp)")
    duration_days = models.IntegerField(verbose_name="Durasi (Hari)")
    max_devices = models.IntegerField(default=1, verbose_name="Batas Perangkat")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Tersedia")
    
    # Method OOP: Tampilan String yang representatif
    def __str__(self):
        return f"{self.name} - Rp{self.price}"

# =======================================================
# MODEL 2: UserSubscription (Objek Langganan User Aktif)
# =======================================================
class UserSubscription(models.Model):
    """Melacak langganan aktif setiap pengguna."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Pengguna")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, verbose_name="Paket Langganan")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Tanggal Mulai")
    end_date = models.DateTimeField(verbose_name="Tanggal Berakhir")
    
    # Method OOP: Enkapsulasi Logika Bisnis
    @property
    def is_active(self):
        """Memeriksa apakah langganan pengguna saat ini masih aktif."""
        return self.end_date >= timezone.now()

    def __str__(self):
        return f"Langganan {self.user.username} ({'Aktif' if self.is_active else 'Kadaluarsa'})"

# =======================================================
# MODEL 3: Transaction (Objek Catatan Transaksi)
# =======================================================
class Transaction(models.Model):
    """Mencatat setiap transaksi pembayaran."""
    STATUS_CHOICES = [
        ('PENDING', 'Menunggu Pembayaran'),
        ('SUCCESS', 'Berhasil'),
        ('FAILED', 'Gagal'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Pengguna")
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Jumlah Pembayaran")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Transaksi")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    
    def __str__(self):
        return f"Transaksi #{self.id} oleh {self.user.username} - Status: {self.status}"
