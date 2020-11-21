from django.contrib import admin
from .models import Fournisseur, Devis, DetailDevis

# Register your models here.
admin.site.register(Fournisseur)
admin.site.register(Devis)
admin.site.register(DetailDevis)
