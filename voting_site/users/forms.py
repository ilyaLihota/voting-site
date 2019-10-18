from django import forms
from django.contrib.auth.hashers import make_password

from users.models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "age",
            "gender",
        )
        widgets = {
            "username": forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Username'}),
            "email": forms.EmailInput(attrs={'class': 'login__input', 'placeholder': 'Email'}),
            "password": forms.PasswordInput(attrs={'class': 'login__input', 'placeholder': 'Password'}),
            "first_name": forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Firstname'}),
            "last_name": forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Lastname'}),
            "age": forms.NumberInput(attrs={'class': 'login__input', 'placeholder': 'Age'}),
            "gender": forms.Select(attrs={'class': 'login__input', 'placeholder': 'Gender'}),
        }

    def save(self, commit=True):
        password = (make_password(self.cleaned_data['password']))
        self.instance.password = password
        self.cleaned_data['password'] = password

        return super().save(commit)
