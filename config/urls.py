# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# --- Imports untuk Pendaftaran (Register) ---
# Mengimpor CreateView untuk membuat view pendaftaran tanpa file views.py baru
from django.views.generic.edit import CreateView 
# Mengimpor UserCreationForm, form bawaan Django untuk registrasi
from django.contrib.auth.forms import UserCreationForm 
# Mengimpor reverse_lazy untuk redirect setelah registrasi
from django.urls import reverse_lazy 


urlpatterns = [
    path('admin/', admin.site.urls),
   path('finance/', include(('finance.urls', 'finance'), namespace='finance')),
    # 1. Login
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='registration/login.html',
             next_page=reverse_lazy('finance:plans') 
         ), 
         name='login'),
         
    # 2. Logout
    path('logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),
    
    # 3. Register 
    path('register/', 
         CreateView.as_view(
             template_name='registration/register.html',
             form_class=UserCreationForm,
             success_url=reverse_lazy('login') 
         ), 
         name='register'), 
]

urlpatterns += [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='root'),
]