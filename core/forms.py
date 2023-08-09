from django import forms

from core.models import User


class AuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', 'password']
