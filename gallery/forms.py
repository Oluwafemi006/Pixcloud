from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ImageGallery, Category

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageGallery
        fields = ['title', 'description', 'image', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }