from django.urls import path

from . import views

app_name = 'gerer_commande'

urlpatterns = [
     path('', views.commandes, name='commandes'),
     
]