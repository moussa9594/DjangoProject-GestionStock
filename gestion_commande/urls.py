from django.urls import path

from . import views

app_name = 'gestion_commande'

urlpatterns = [
     path('categorie/<int:id_categorie>', views.produit_by_categorie, name='produits'),
     path('connexion/', views.login, name='login'),
     path('connexion/logout', views.logout, name='logout'),
    #  path('categorie/<int:id_categorie>', views.produit_by_categorie, name='produits'),
     path('', views.produit, name='produit'),
     path('add-order', views.add_order, name='add_order'),
     path('panier/', views.mon_panier, name='mon_panier'),
     path('panier/save-qte', views.panier, name='panier'),
     path('panier/<int:id_produit>/quantite', views.add_quantite, name='add_quantite'),
     path('panier/save', views.save_commande, name='save_commande'),
     path('panier/delete', views.delete_commande, name='delete_commande'),
     path('panier/connexion', views.connexion, name='connexion'),
     path('panier/orders', views.mes_commandes, name='mes_commandes'),
     path('panier/orders/<int:id_commande>', views.detail_commande, name='detail_commande'),
     path('panier/connexion/valid', views.valid_connexion, name='valid_connexion'),
     path('panier/connexion/check', views.check_connexion, name='check_connexion'),
     path('produit/<int:id_produit>', views.detail, name='detail'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]