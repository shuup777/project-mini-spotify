
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils import timezone
from django.core.paginator import Paginator
from .models import SubscriptionPlan, Subscription, Transaction
from decimal import Decimal
import datetime 


class PlanListView(ListView):
    model = SubscriptionPlan
    template_name = 'finance/plan_list.html'
    context_object_name = 'object_list'
    ordering = ['price']
plan_list = PlanListView.as_view()


@login_required
def checkout(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    if request.method == 'POST':
        DURATION = 30 
        
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            defaults={
                'plan': plan, 
                'end_date': timezone.now() + datetime.timedelta(days=DURATION)
            }
        )
        
        if not created:
            subscription.plan = plan
            subscription.end_date = timezone.now() + datetime.timedelta(days=DURATION)
            subscription.is_active = True
            subscription.save()
            
        # 2. Catat Transaksi
        Transaction.objects.create(
            user=request.user,
            plan=plan,
            amount=plan.price,
            status='SUCCESS' 
        )

        return redirect('finance:payment_success')

    context = {'plan': plan}
    return render(request, 'finance/checkout.html', context)

# --- View Sukses Pembayaran ---
@login_required
def payment_success(request):
    return render(request, 'finance/payment_success.html')

# --- View Detail Langganan ---
@login_required
def subscription_detail(request):
    try:
        subscription = request.user.subscription 
        if subscription.is_expired():
             subscription.is_active = False
             subscription.save()
    except Subscription.DoesNotExist:
        subscription = None 

    context = {'subscription': subscription}
    return render(request, 'finance/subscription_detail.html', context)

# --- View Laporan Keuangan ---
@login_required
def report(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('plan_list') 
    
    transactions = Transaction.objects.all().order_by('-transaction_date')

    status_filter = request.GET.get('status')
    min_amount_str = request.GET.get('min_amount')
    min_amount = None

    if status_filter:
        transactions = transactions.filter(status=status_filter)
    
    if min_amount_str:
        try:
            min_amount = Decimal(min_amount_str)
            transactions = transactions.filter(amount__gte=min_amount)
        except:
            pass 
    

    successful_transactions = Transaction.objects.filter(status='SUCCESS')
    total_revenue = sum(t.amount for t in successful_transactions)
    pelanggan_aktif = Subscription.objects.filter(is_active=True).count() 
    total_transaksi = Transaction.objects.all().count()

    paginator = Paginator(transactions, 20) 
    page_number = request.GET.get('page')
    transaksi_halaman = paginator.get_page(page_number)
    
    context = {
        'transaksi_halaman': transaksi_halaman,
        'total_pendapatan': total_revenue, 
        'pelanggan_aktif': pelanggan_aktif, 
        'total_transaksi': total_transaksi, 

        'status_choices': Transaction.STATUS_CHOICES,
        'status_filter': status_filter,
        'min_amount': min_amount,
    }
    return render(request, 'finance/report.html', context)