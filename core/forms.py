# core/forms.py

from django import forms
from .models import User, Donation

class DonorSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'organization_name', 'email', 'phone_number', 'address', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.user_type = 1 # Donor
        if commit:
            user.save()
        return user

class NgoSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'organization_name', 'email', 'phone_number', 'address', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.user_type = 2 # NGO
        if commit:
            user.save()
        return user

class DonationForm(forms.ModelForm):
    pickup_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    class Meta:
        model = Donation
        fields = ['food_description', 'quantity', 'pickup_location', 'pickup_time']