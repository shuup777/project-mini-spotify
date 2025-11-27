# finance/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta 
from .models import SubscriptionPlan, UserSubscription, Transaction 
# Pastikan semua Model diimpor

def plan_list(request):
    """
    Menampilkan daftar semua paket langganan yang tersedia (Admin Keuangan).
    """
    # Mengambil semua paket yang aktif, diurutkan berdasarkan harga.
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
    
    context = {
        'plans': plans,
        'page_title': 'Pilih Paket Langganan Mini Spotify'
    }
    
    return render(request, 'finance/plan_list.html', context)

@login_required 
def checkout_view(request, plan_id):
    """
    Memproses permintaan langganan dan mencatat Transaksi/Langganan.
    Ini adalah logika yang dipicu saat tombol 'Langganan Sekarang' diklik.
    """
    
    # 1. Ambil Objek Paket dan User yang Login
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    user = request.user
    
    # 2. Logika Sederhana Pembayaran (Disini Anda akan menambahkan integrasi Payment Gateway nanti)
    
    # 3. Catat Transaksi
    Transaction.objects.create(
        user=user,
        amount=plan.price,
        status='SUCCESS' 
    )
    
    # 4. Hitung Tanggal Berakhir
    end_date = timezone.now() + timedelta(days=plan.duration_days)
    
    # 5. Aktifkan/Perbarui Langganan User
    UserSubscription.objects.update_or_create(
        user=user,
        defaults={
            'plan': plan,
            'end_date': end_date
        }
    )
    
    # 6. Redirect ke halaman sukses
    return redirect('subscription_success') 

def success_view(request):
    """Halaman sukses setelah langganan."""
    return render(request, 'finance/success.html', {'message': 'Langganan Anda berhasil diaktifkan!'})