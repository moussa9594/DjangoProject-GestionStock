from django.urls import path

from . import views

app_name = 'gestion_fournisseur'

urlpatterns = [
     path('', views.fournisseur, name='fournisseur'),
     path('create/fournisseur', views.create_fournisseur, name='create_fournisseur'),
     path('detail/fournisseur/<int:id_fournisseur>', views.detail_fournisseur, name='detail'),
     path('demande/fournisseur/<int:id_fournisseur>', views.demande, name='demande'),
     path('demande/fournisseur/<int:id_fournisseur>/historique', views.historique, name='historique'),
     path('demande/fournisseur', views.add_demande, name='add_demande'),
     path('demande/fournisseur-send', views.sendmail, name='send_mail'),
     path('save/fournisseur', views.save_fournisseur, name='save_fournisseur'),
     path('devis/etat', views.approuver_demande, name='approuver_demande'),
     path('devis/etat/<int:id_devis>/valider', views.valider_devis, name='valider_devis'),
     path('devis/etat/change/<int:id_devis>', views.change_etat_devis, name='change_etat_devis'),
     path('devis/etat/<int:id_devis>', views.voir_devis, name='voir_devis'),
     path('devis/etat/<int:id_devis>/delete', views.delete_devis, name='delete_devis'),
]