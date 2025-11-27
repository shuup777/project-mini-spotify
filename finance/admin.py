from django.contrib import admin

# finance/admin.py
from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, Transaction

# Opsi: Tambahkan tampilan daftar (list_display) untuk kemudahan manajemen
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'start_date')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'timestamp', 'status')
    list_filter = ('status', 'timestamp')

admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
admin.site.register(Transaction, TransactionAdmin)
