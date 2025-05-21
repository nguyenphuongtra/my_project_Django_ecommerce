from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(UserChangeForm):
    password = None  
    avatar = forms.ImageField(
        required=False, 
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']
