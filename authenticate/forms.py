from django import forms
from .models import Login

class LoginForm(forms.Form):
    model = Login
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'password': forms.PasswordInput(),
        }
    fields = ('email','password')