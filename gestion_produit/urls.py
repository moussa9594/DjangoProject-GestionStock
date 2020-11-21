from django.urls import path

from . import views

app_name = 'gestion_produit'

urlpatterns = [
     path('categorie/<int:id_categorie>', views.produit, name='produit'),
     path('<int:id_produit>/', views.detail, name='detail'),
     path('create/produit/devis/<int:id_detail_devis>', views.create_produit, name='create_produit'),
     path('save/produit', views.save_produit, name='save_produit'),
     path('delete/produit/<int:id_produit>', views.delete_produit, name='delete_produit'),
     path('edit/produit/<int:id_produit>', views.edit_produit, name='edit_produit'),
     path('save-edit/produit/<int:id_produit>', views.save_edit_produit, name='save_edit_produit'),
     path('produit/select-devis', views.select_devis, name='select_devis'),
]