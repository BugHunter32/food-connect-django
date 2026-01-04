# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/donor/', views.donor_signup, name='donor_signup'),
    path('signup/ngo/', views.ngo_signup, name='ngo_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/donor/', views.donor_dashboard, name='donor_dashboard'),
    path('donation/new/', views.create_donation, name='create_donation'),
    
    path('dashboard/ngo/', views.ngo_dashboard, name='ngo_dashboard'),
    path('donation/claim/<int:donation_id>/', views.claim_donation, name='claim_donation'),
]