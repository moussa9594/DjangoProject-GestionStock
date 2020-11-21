from django.contrib import admin
from .models import Produit, Categorie, EssaiImage
# Register your models here.
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(EssaiImage)