# finance/admin.py
from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Transaction

# --- Koreksi SubscriptionPlanAdmin ---
class SubscriptionPlanAdmin(admin.ModelAdmin):
    # 'duration_days' dihapus, hanya menyisakan 'name' dan 'price'
    list_display = ('name', 'price',) 
    search_fields = ('name',)

# --- Perbaikan Model Transaction (menambahkan 'status' yang hilang) ---
# Sebelum mengedit TransactionAdmin, kita tambahkan field STATUS di model Transaction
# Asumsi Anda ingin menambahkan Status transaksi. Jika tidak, hapus saja 'status' dari list_display di bawah.
# CATATAN: Karena model Transaction Anda TIDAK memiliki field 'status',
# kita akan menghapusnya dari admin.py agar tidak error.

class TransactionAdmin(admin.ModelAdmin):
    # Mengoreksi 'subscription_plan' menjadi 'plan'
    list_display = ('user', 'plan', 'amount', 'transaction_date',)
    list_filter = ('plan', 'transaction_date',) # Mengganti 'subscription_plan' menjadi 'plan'
    search_fields = ('user__username', 'plan__name',)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active',)
    list_filter = ('is_active', 'plan',)
    search_fields = ('user__username', 'plan__name',)
    # Menambahkan field 'is_active' agar bisa diubah dengan cepat
    list_editable = ('is_active',) 


# Daftarkan Model di Admin
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Transaction, TransactionAdmin)