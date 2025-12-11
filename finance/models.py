
from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal 
User = settings.AUTH_USER_MODEL 

# 1. MODEL SUBSCRIPTION PLAN 
class SubscriptionPlan(models.Model):
    BASIC = 'BAS'
    PREMIUM = 'PRE'
    FAMILY = 'FAM'
    
    NAME_CHOICES = [
        (BASIC, 'Basic (Hanya 1 perangkat, Kualitas Standar)'),
        (PREMIUM, 'Premium (Bebas iklan, Kualitas HD, 2 perangkat)'),
        (FAMILY, 'Family (Bebas iklan, Kualitas HD, Hingga 6 perangkat)'),
    ]
    
    name = models.CharField(max_length=3, choices=NAME_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=0) 
    
    def __str__(self):
        return self.get_name_display()

# 2. MODEL SUBSCRIPTION
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_expired(self):
        return self.end_date < timezone.now()

    def save(self, *args, **kwargs):
        if not hasattr(self, '_original_plan_id'):
            self._original_plan_id = self.plan_id
            
        if not self.pk or self.plan_id != self._original_plan_id:
            self.end_date = timezone.now() + timedelta(days=30)
            self.is_active = True 
            
        super().save(*args, **kwargs)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_plan_id = self.plan_id

    def __str__(self):
        return f"Langganan {self.user.username} - {self.plan.get_name_display() if self.plan else 'Tanpa Paket'}"

# 3. MODEL TRANSACTION 
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Berhasil'),
        ('PENDING', 'Menunggu Pembayaran'),
        ('FAILED', 'Gagal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SUCCESS')
    
    def __str__(self):
        return f"Transaksi {self.id} oleh {self.user.username} - Rp{self.amount} ({self.get_status_display()})"