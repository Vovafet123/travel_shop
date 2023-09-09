from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import User


class AuthRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['login']
