"""
URL configuration for mini_spotify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys
import os

project_path = r"C:\Users\Lenovo\Documents\project-mini-spotify"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

from django.contrib import admin
from django.urls import path, include
from user_app import views as user_views  
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_views.home, name='home'),  
    path('admin/', admin.site.urls),
    path('system/', include('system_admin_app.urls')),
    path('user/', include('user_app.urls')),
    path('artist/', include('artist_app.urls')),
    path('finance/', include('finance_app.urls')),

    # login
    path( 'accounts/login/',
    auth_views.LoginView.as_view(template_name='login.html'),
    name='login')
]
