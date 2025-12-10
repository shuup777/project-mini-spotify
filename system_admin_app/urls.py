from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "system_admin_app"

urlpatterns = [
    path('', views.dashboard, name="system-dashboard"),
    path('admin/', admin.site.urls),
    path('user/', include('user_app.urls')),
    path('recommendations/', views.recommendations, name="recommendations"),
]