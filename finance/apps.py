# finance/apps.py
from django.apps import AppConfig
from django.conf import settings
from decimal import Decimal
from django.db.models import Field 
import inspect # PENTING: Untuk memeriksa tanda tangan fungsi

def apply_sqlite_decimal_fix():
    if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
        return

    try:
        from django.db.backends.sqlite3.operations import DatabaseOperations

        def lookup_cast_fix(self, lookup, field=None, value=None):
            
            # --- 1. Tentukan Tipe Field Internal ---
            if isinstance(field, Field):
                field_internal_type = field.get_internal_type()
            elif isinstance(field, str):
                # Kasus lama: field_internal_type dikirim sebagai string
                field_internal_type = field 
            else:
                field_internal_type = None

            # --- 2. Terapkan Perbaikan DecimalField ---
            # Hanya berlaku jika tipenya adalah DecimalField dan ada nilai Decimal yang dibandingkan
            if field_internal_type == 'DecimalField' and value is not None:
                if lookup in ('exact', 'lte', 'lt', 'gte', 'gt') and isinstance(value, Decimal):
                    return float(value)
            
            # --- 3. Panggil Metode Asli dengan Jumlah Argumen yang Benar ---
            original_func = self.lookup_cast_original
            # Dapatkan jumlah argumen wajib (dikurangi self)
            arg_spec = inspect.getfullargspec(original_func)
            arg_count = len(arg_spec.args) - 1 # Kurangi 'self'

            if arg_count == 3:
                # Metode asli menerima (lookup, field, value)
                return original_func(lookup, field, value)
            elif arg_count == 2:
                # Metode asli menerima (lookup, field_internal_type). 
                # Kita harus meneruskan field_internal_type (string) sesuai varian lama.
                return original_func(lookup, field_internal_type)
            else:
                # Fallback untuk kasus tak terduga
                # Kita harus tetap mencoba meneruskan field_internal_type
                # Jika metode aslinya sangat kuno dan hanya menerima 2 argumen.
                return original_func(lookup, field_internal_type)

        
        if not hasattr(DatabaseOperations, 'lookup_cast_original'):
            DatabaseOperations.lookup_cast_original = DatabaseOperations.lookup_cast
            DatabaseOperations.lookup_cast = lookup_cast_fix
            
    except ImportError:
        pass


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'
    
    def ready(self):
        apply_sqlite_decimal_fix()