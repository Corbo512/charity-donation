from django import forms
from .models import User
from django.contrib.auth import authenticate


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean(self):
        cleaned_data = super().clean()

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', 'Hasła nie są takie same')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Konto o takim adresie email już istnieje')
        return cleaned_data

class UserLoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'form-group',
                   'type': 'email',
                   'placeholder': 'Email'
                   })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-group',
                   'type': 'password',
                   'placeholder': 'Hasło'
                   })
    )
