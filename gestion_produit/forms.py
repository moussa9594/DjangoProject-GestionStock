from django import forms
from .models import Produit, Categorie
from employe.models import Employe

categories = Categorie.objects.all()

class CategorieForm(forms.Form):
    libelle = forms.CharField(max_length=100)


class ProduitForm(forms.ModelForm):
    # libelle = forms.CharField(max_length=100)
    # prix_u = forms.IntegerField()
    # quantite = forms.IntegerField()
    # description = forms.CharField(max_length=300)
    # categorie = forms.ModelMultipleChoiceField(queryset=categories)
    class Meta:
        model = Produit
        fields = '__all__'