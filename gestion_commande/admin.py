from django.contrib import admin
from .models import Client, Commande, LigneCommande

# Register your models here.
admin.site.register(Client)
admin.site.register(Commande)
admin.site.register(LigneCommande)
