from django.db import models
from employe.models import Employe
from gestion_fournisseur.models import Fournisseur


    # get fournisseur
    # 
# Create your models here.
class Categorie(models.Model):
    libelle = models.CharField(max_length=100)
    def __str__(self):
        return self.libelle

class Produit(models.Model):
    image1 =models.ImageField(upload_to='images/', null = True)
    image2 =models.ImageField(upload_to='images/', null = True)
    libelle = models.CharField(max_length=100)
    prix_u = models.BigIntegerField()
    quantite = models.IntegerField()
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, default = None)

class EssaiImage(models.Model):
    image =models.ImageField(upload_to='images/', null = True)



    