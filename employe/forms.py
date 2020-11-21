from django.db import models
from django import forms
from .models import Employe, Message

# Create your models here.

class EmployeForm(forms.Form):
    class Meta:
        model = Employe
        widgets = {
        'password': forms.PasswordInput(),
        }
        fields = ('prenom','nom','sexe','telephone','email','login','role','password','adresse')
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'