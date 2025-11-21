from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('artist/', include('artist_app.urls')),
    path('user/', include('user_app.urls')),
    path('system/', include('system_admin_app.urls')),
    path('finance/', include('finance_app.urls')),
]
