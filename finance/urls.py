
from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.report, name='report'), 
    path('plans/', views.PlanListView.as_view(), name='plans'),
    path('checkout/<int:plan_id>/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('detail/', views.subscription_detail, name='subscription_detail'),
]