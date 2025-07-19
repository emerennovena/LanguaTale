from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class CustomSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'username': forms.TextInput(attrs={'class': 'input-field'}),
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
            'password1': forms.PasswordInput(attrs={'class': 'input-field'}),
            'password2': forms.PasswordInput(attrs={'class': 'input-field'}),
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'input-field'})
        self.fields['password'].widget.attrs.update({'class': 'input-field'})
