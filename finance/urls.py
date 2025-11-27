from django.urls import path
from . import views

urlpatterns = [
    # Path: /finance/plans/
    path('plans/', views.plan_list, name='plan_list'),
    path('checkout/<int:plan_id>/', views.checkout_view, name='checkout'),
    path('success/', views.success_view, name='subscription_success'),
]