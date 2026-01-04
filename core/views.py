# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import DonorSignUpForm, NgoSignUpForm, DonationForm
from .models import Donation, User

def home(request):
    return render(request, 'core/home.html')

def donor_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = DonorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('donor_dashboard')
    else:
        form = DonorSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'user_type': 'Donor'})

def ngo_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = NgoSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ngo_dashboard')
    else:
        form = NgoSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'user_type': 'NGO'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 1:
                    return redirect('donor_dashboard')
                elif user.user_type == 2:
                    return redirect('ngo_dashboard')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def donor_dashboard(request):
    if request.user.user_type != 1:
        return redirect('home')
    donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
    return render(request, 'core/donor_dashboard.html', {'donations': donations})

@login_required
def create_donation(request):
    if request.user.user_type != 1:
        return redirect('home')
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            return redirect('donor_dashboard')
    else:
        form = DonationForm()
    return render(request, 'core/donation_form.html', {'form': form})

@login_required
def ngo_dashboard(request):
    if request.user.user_type != 2:
        return redirect('home')
    available_donations = Donation.objects.filter(
        status='available', 
        pickup_time__gte=timezone.now()
    ).order_by('pickup_time')
    claimed_donations = Donation.objects.filter(claimed_by=request.user).exclude(status='delivered').order_by('pickup_time')
    return render(request, 'core/ngo_dashboard.html', {
        'available_donations': available_donations,
        'claimed_donations': claimed_donations
    })

@login_required
def claim_donation(request, donation_id):
    if request.user.user_type != 2:
        return redirect('home')
    donation = get_object_or_404(Donation, id=donation_id)
    if donation.status == 'available':
        donation.claimed_by = request.user
        donation.status = 'claimed'
        donation.save()
    return redirect('ngo_dashboard')