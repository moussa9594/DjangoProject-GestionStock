from django.db import models
from gestion_produit.models import Produit

# # Create your models here.
class Client(models.Model):
    sexe = [('Masculin','Masculin'),('Feminin','Feminin')]
    # role = [('g_p','Gestionnaire de produits'),('g_c','Gestionnaire de commande')]
    # 
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices = sexe, default = 'Masculin')
    telephone = models.CharField(max_length=100)
    email = models.EmailField()
    login = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100)
    adresse = models.TextField() 
    def __str__(self):
        return self.prenom + " " +self.nom

class Commande(models.Model):
    date_commande = models.DateTimeField(auto_now=True)
    nbre_produit = models.IntegerField()
    prix_total = models.IntegerField()
    etat = models.IntegerField(default = 0)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default = 1)
    
class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveSmallIntegerField()
    sous_total = models.BigIntegerField()
    

    