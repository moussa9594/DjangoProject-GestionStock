from django.db import models
# from django import forms
import datetime
# Create your models here.

class Employe(models.Model):
    sexe = [('Masculin','m'),('Feminin','f')]
    role = [
        ('g_p','Gestionnaire de produits'),
        ('g_c','Gestionnaire de commande'),
        ('g_f','Gestionnaire de fournisseur')]
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices = sexe, default = 'Masculin')
    telephone = models.CharField(max_length=100)
    email = models.EmailField()
    login = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100)
    adresse = models.TextField() 
    role = models.CharField(max_length=10, choices = role, default = 'g_p')
    def __str__(self):
        return self.prenom + " " +self.nom

class Message(models.Model):
    objet = models.CharField(max_length=100, default='', null = True)
    destinataire = models.EmailField(null = True)
    text = models.TextField()
    lire = models.IntegerField(default = 0)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date = models.DateField(default = datetime.date.today())
    

    
