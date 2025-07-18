from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input-field'
            }),

            'username': forms.TextInput(attrs={
                'class': 'input-field'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'input-field'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'input-field'
            }),
        }
