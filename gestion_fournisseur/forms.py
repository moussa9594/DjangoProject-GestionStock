from django.db import models
from django import forms
from .models import Fournisseur
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator
# Create your models here.

class FournisseurForm(forms.Form):
    # model = Fournisseur
    sexes = [('Masculin','Masculin'),('Feminin','Feminin')]
    # 
    prenom = forms.CharField(max_length=100)
    nom = forms.CharField(max_length=100)
    sexe = forms.MultipleChoiceField(choices=sexes)
    telephone = forms.CharField(max_length=9, validators='[0-9]') # validators should be a list
    email = forms.EmailField()
    adresse = forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 5}))
    
    fields = ('prenom','nom','sexe','telephone','email','adresse')