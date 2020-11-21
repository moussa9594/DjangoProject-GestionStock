from django.shortcuts import render, get_object_or_404
from gestion_produit.models import Produit, Categorie
from employe.models import Employe
from .models import Client, Commande, LigneCommande
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def produit(request):
        client = None
        if 'id_client' in request.session:
            client = Client.objects.get(id = request.session.get('id_client'))
        categories = Categorie.objects.all()
        mes_produits = []
        for categorie in categories:
            produits = Produit.objects.filter(categorie = categorie)[:2]
            for produit in produits:
                mes_produits.append(produit)
        panier = ''
        if request.session.get('panier') != None:
            panier = request.session.get('panier')
    # verifier si des produits sont disponibles en stock
        return render(request, 'commande/index.html', {
        'mes_produits': mes_produits,
        'categories': categories,
        'panier': len(panier),
        'client': client
    })

def produit_by_categorie(request, id_categorie):
        client = None
        if 'id_client' in request.session:
            client = Client.objects.get(id = request.session.get('id_client'))
        categories = Categorie.objects.all()
        categorie = Categorie.objects.get(id=id_categorie)
        produit_list = Produit.objects.filter( categorie = categorie)
        panier = ''
        if request.session.get('panier') != None:
            panier = request.session.get('panier')
    # verifier si des produits sont disponibles en stock
        return render(request, 'commande/index.html', {
        'produit_list': produit_list,
        'panier': len(panier),
        'categories': categories,
        'client': client,
        'same_categorie': categorie,
    })
    # except:
    #     return HttpResponseRedirect('/' )
    
def detail(request, id_produit):
    client = None
    if 'id_client' in request.session:
            client = Client.objects.get(id = request.session.get('id_client'))
    produit = Produit.objects.get(id = id_produit)
    produit = Produit.objects.get(id=id_produit)
    categorie = Categorie.objects.get(id=produit.categorie.id)
    categories = Categorie.objects.all()
    panier = ''
    if request.session.get('panier') != None:
            panier = request.session.get('panier')
    # verifier si des produits sont disponibles en stock
    
    return render(request, 'commande/detail.html', 
    {'produit': produit, 
        'panier': len(panier),
    'categories': categories,
    'client': client,
    'same_categorie': categorie,
    })


def panier(request):
    id_produit = int(request.GET['produit'])
    quantite = int(request.GET['quantite'])
    if 'panier' not in request.session:
        panier = {}
        panier[id_produit] = quantite
        request.session['panier'] = panier
    else:
        panier = request.session.get('panier')
        panier[id_produit] = quantite
    request.session['panier'] = panier
    categories = Categorie.objects.all()
    produit = Produit.objects.get(id=id_produit)
    categorie = Categorie.objects.get(id=produit.categorie.id)
    produit_list = Produit.objects.filter( categorie = categorie)
    # verifier si des produits sont disponibles en stock
    return HttpResponseRedirect('/boutique/categorie/' + str(categorie.id) )
    # return render(request, 'commande/index.html', {
    #     'produit_list': produit_list,
    #     'categories': categories,
    #     'same_categorie': categorie,
    #     'panier': len(panier),
    # })
def add_quantite(request,id_produit):
    client = None
    if 'id_client' in request.session:
            client = Client.objects.get(id = request.session.get('id_client'))
    quantite_exist = None
    sous_total_exist = None
    produit = Produit.objects.get(id = id_produit)
    categories = Categorie.objects.all()
    if 'panier' in request.session:
        panier = request.session.get('panier')
        if str(id_produit) in panier:
            quantite_exist = panier[str(id_produit)]
            sous_total_exist = quantite_exist * produit.prix_u
    return render(request, 'commande/add_quantite.html', 
    {'produit': produit, 
    'categories': categories,
    'client': client,
    'quantite_exist': quantite_exist,
    'sous_total_exist': sous_total_exist,
    })

def mon_panier(request):
        panier = request.session.get('panier')
        categories = Categorie.objects.all()
        client = None
        if 'id_client' in request.session:
            client = Client.objects.get(id = request.session.get('id_client'))
        try:
            produits = []
            soustotals = []
            for id in panier:
                produits.append(
                    Produit.objects.get(id = str(id))
                )
            for produit in produits:
                for id_produit in panier:
                    if produit.id == int(id_produit):
                        soustotals.append(
                        panier[id_produit] * 
                        produit.prix_u
                    )
        
            total = sum(soustotals)
            request.session['total'] = total
    # verifier si des produits sont disponibles en stock
        except:
            return HttpResponseRedirect('/boutique/panier/delete' )
        return render(request, 'commande/mon_panier.html', {
        'panier': len(panier),
        'categories': categories,
        'produits': produits,
        'paniers': panier,
        'soustotals': soustotals,
        'client': client,
        'total': total,
    })

            
        
def save_commande(request):
    panier = request.session.get('panier')
    
    del request.session["panier"]
    return HttpResponseRedirect('/boutique' )

def delete_commande(request):
    panier = request.session.get('panier')
    del request.session["panier"]
    return HttpResponseRedirect('/boutique' )

def connexion(request):
    panier = request.session.get('panier')
    return render(request, 'commande/connexion_client.html', {
       'panier': len(panier),
    })

def valid_connexion(request):
    panier = request.session.get('panier')
    prenom = request.POST['prenom']
    nom = request.POST['nom']
    telephone = request.POST['telephone']
    email = request.POST['email']
    sexe = request.POST['sexe']
    adresse = request.POST['adresse']
    login = request.POST['login']
    password = request.POST['password']
    client = None
    commande = None
    client_exist = None
    try:
        #vérifier si le client existe dans la base
        client_exist = Client.objects.get(login = login) 
        if client_exist != None:
            error = "Ce login existe déjà ."
            return render(request, 'commande/connexion_client.html', {
       'panier': len(panier), 'error': error
        })
    except:
        pass
    try:
        
        # insère dans client
        client = Client.objects.create(
            prenom = prenom, nom = nom, telephone = telephone, sexe = sexe, email = email,
            adresse = adresse, login = login, password = password,
        )
        request.session['id_client'] = client.id
        return HttpResponseRedirect('/boutique' )
        
    except:
        error = "enregistrement dans client échoué"
        return render(request, 'commande/connexion_client.html', {
       'panier': len(panier), 'error': error
    })
   
def check_connexion(request):
    panier = request.session.get('panier')
    login = request.POST['login']
    password = request.POST['password']
    client_exist = None
    commande = None
    try:
        client_exist = Client.objects.get(login = login, password = password)
        request.session['id_client'] = client_exist.id
        return HttpResponseRedirect('/boutique' )
    except:
            error = "login ou mot de passe incorrect"
            return render(request, 'commande/connexion_client.html', {
            'panier': len(panier), 'error': error
            })

def add_order(request):
    panier = request.session.get('panier')
    if 'id_client' in request.session:
        id_client = request.session.get('id_client')
        client = Client.objects.get(id = id_client)
        # inserer commande
        try:
           # insertion dans commande
            if 'total' in request.session:
                total = request.session.get('total')
            else:
                total = 0
            commande = Commande.objects.create(
                client = client, nbre_produit = len(panier), prix_total = total
            )
        except:
            error = "enregistrement dans commande échoué"
            return render(request, 'commande/connexion_client.html', {
        'panier': len(panier), 'error': error
        })
        try:
            # insère dans ligne_commande et garder la session du client
            # liste des produits commandés
            produits = []
            soustotals = []
            for id in panier:
                produits.append(
                    Produit.objects.get(id = str(id)))
        # parcourir la liste des produits commandés et calculé 
        # le sous total pour chaque produit et en même temps insérer
            for produit in produits:
                for id_produit in panier:
                    if produit.id == int(id_produit):
                        soustotal = panier[id_produit] * produit.prix_u
                        # insertion
                        LigneCommande.objects.create(commande = commande, produit = produit,  
                                                    quantite = panier[id_produit], sous_total = soustotal)
                        # decrementé le stock
                        Produit.objects.filter(id = produit.id).update(quantite = produit.quantite - panier[id_produit])
            request.session['id_client'] = client.id
        except:
            error = "enregistrement dans ligne_commande échoué"
            return render(request, 'commande/connexion_client.html', {
        'panier': len(panier), 'error': error
        })
        return HttpResponseRedirect('/boutique/panier/delete' )
    else:
        # rediriger dans la page de connexion
        return HttpResponseRedirect('/boutique/connexion' )

def mes_commandes(request):
    panier = ''
    if 'panier' in request.session:
        panier = request.session.get('panier')
    categories = Categorie.objects.all()
    if 'id_client' in request.session:
        id_client = request.session.get('id_client')
        client = Client.objects.get(id = id_client)
        mes_commandes = Commande.objects.filter(client = client)
        return render(request, 'commande/mes_commandes.html', {
            'client': client,
            'panier': len(panier),
            'categories': categories,
            'mes_commandes': mes_commandes
        })
    else:
        return HttpResponseRedirect('/boutique/connexion' )

def detail_commande(request, id_commande):
    panier = ''
    if 'panier' in request.session:
        panier = request.session.get('panier')
    categories = Categorie.objects.all()
    if 'id_client' in request.session:
        id_client = request.session.get('id_client')
        client = Client.objects.get(id = id_client)
        commande = Commande.objects.get(id = id_commande)
        ligne_commande = LigneCommande.objects.filter(commande = commande)
        return render(request, 'commande/detail_commande.html', {
            'client': client,
            'panier': len(panier),
            'categories': categories,
            'ligne_commande': ligne_commande,
            'commande': commande
        })
    else:
        return HttpResponseRedirect('/boutique/connexion' )
   
def login(request):
    panier = ''
    if 'panier' in request.session:
        panier = request.session.get('panier')
    return render(request, 'commande/connexion_client.html', {
            'panier': len(panier)
            })
def logout(request):
    del request.session['id_client']
    return HttpResponseRedirect('/boutique' )


