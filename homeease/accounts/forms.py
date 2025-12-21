from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users with all required fields
    """
    
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_numberr',
            'address',
            'gender',
            'password1',
            'password2'
        )