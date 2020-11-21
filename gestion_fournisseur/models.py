from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.
class Fournisseur(models.Model):
    sexe = [('Masculin','Masculin'),('Feminin','Feminin')]
    # 
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices = sexe, default = 'Masculin')
    telephone = models.CharField(max_length=9)
    email = models.EmailField()
    adresse = models.TextField()
    def __str__(self):
        return self.prenom + " " +self.nom

class Devis(models.Model):
    date_devis = models.DateField()
    nbre_produit = models.IntegerField(default = 0)
    etat = models.IntegerField(default = 0)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    

class DetailDevis(models.Model):
    libelle = models.CharField(max_length=100)
    quantite = models.IntegerField()
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE)
    ajouter = models.IntegerField(default = 0)
