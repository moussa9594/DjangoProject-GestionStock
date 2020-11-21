from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Produit, Categorie
from employe.models import Employe, Message
from .forms import ProduitForm
from django.http import HttpResponse, HttpResponseRedirect
from gestion_fournisseur.models import Devis, DetailDevis

# Create your views here.

def produit(request, id_categorie):
    # try:
        if request.session.get('id_employe') == None:
            return HttpResponseRedirect('/' ) 
        id_employe = request.session.get('id_employe')
        employe_login = Employe.objects.get(id = id_employe)
        if employe_login.role != "g_p":
            return HttpResponseRedirect('/' ) 
        categories = Categorie.objects.all()
        categorie = Categorie.objects.get(id=id_categorie)
        produit_list = Produit.objects.filter( categorie = categorie)
        for p in produit_list:
                print(p.image1)
            
    # verifier si des produits sont disponibles en stock
        try:
            devis = Devis.objects.get(etat = 1)
            all_detail_devis = DetailDevis.objects.filter(ajouter = 0, devis = devis.first())
        except:
            all_detail_devis = []
            detail_devis = DetailDevis.objects.filter(ajouter = 0)
            for detail in detail_devis:
                if detail.devis.etat == 1:
                    all_detail_devis.append(detail)
        messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
        return render(request, 'produit/index.html', {
        'produit_list': produit_list,
        'employe_login': employe_login,
        'categories': categories,
        'same_categorie': categorie,
        'all_detail_devis': all_detail_devis,
        'messages': messages,
    })
    # except:
    #     return HttpResponseRedirect('/' )
    
def detail(request, id_produit):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_p":
        return HttpResponseRedirect('/' ) 
    produit = Produit.objects.get(id = id_produit)
    categories = Categorie.objects.all()
    # verifier si des produits sont disponibles en stock
    try:
        devis = Devis.objects.get(etat = 1)
        all_detail_devis = DetailDevis.objects.filter(ajouter = 0, devis = devis.first())
    except:
        all_detail_devis = []
        detail_devis = DetailDevis.objects.filter(ajouter = 0)
        for detail in detail_devis:
            if detail.devis.etat == 1:
                all_detail_devis.append(detail)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'produit/detail.html', 
    {'produit': produit, 
    'categories': categories,
    'employe_login': employe_login,
        'same_categorie': produit.categorie,
    'messages': messages,
    'all_detail_devis': all_detail_devis,})

def create_produit(request, id_detail_devis):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' ) 
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_p":
        return HttpResponseRedirect('/' ) 
     # verifier si des produits sont disponibles en stock
    try:
        devis = Devis.objects.get(etat = 1)
        all_detail_devis = DetailDevis.objects.filter(ajouter = 0, devis = devis.first())
    except:
        all_detail_devis = []
        detail_devis = DetailDevis.objects.filter(ajouter = 0)
        for detail in detail_devis:
            if detail.devis.etat == 1:
                all_detail_devis.append(detail)   
    # changer l attribut "ajouter" dans devis pour le mettre dans detail devis
    # et a chaque fois qu on ajoute le detail devis on le change a 1.
    # Revoir la requete qui selectionne les devis non ajouter a la base 
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )  
    categories = Categorie.objects.all()
    detail_devis = DetailDevis.objects.get(id = id_detail_devis)
    produit_existe = Produit.objects.get(libelle = detail_devis.libelle)
    if produit_existe != None:
        qt = produit_existe.quantite + detail_devis.quantite
        Produit.objects.filter(id = produit_existe.id).update(quantite = qt )
        return HttpResponseRedirect('/gestion_produit/categorie/' + str(produit_existe.categorie.id) )
    else:
        request.session["id_detail_devis"] = id_detail_devis
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'produit/create_produit.html', 
        {'detail_devis': detail_devis, 
        'employe_login': employe_login,
         'messages': messages,
        'categories': categories, 
        'all_detail_devis': all_detail_devis,})

def select_devis(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )  
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_p":
        return HttpResponseRedirect('/' )   
    devis = Devis.objects.filter(etat = 1)
    detail_devis = DetailDevis.objects.filter(ajouter = 0)
    all_detail_devis = []
    for detail in detail_devis:
        if detail.devis.etat == 1:
            all_detail_devis.append(detail)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'produit/select_devis.html', 
    {'all_detail_devis': all_detail_devis,
        'employe_login': employe_login,
    'messages': messages,
    })

def save_produit(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_p":
        return HttpResponseRedirect('/' ) 
    # init produit
    id_detail_devis = int(request.session.get("id_detail_devis"))
    detail_devis = DetailDevis.objects.get(id = id_detail_devis)
    libelle = request.POST['libelle']
    image1 = 'images/' + request.POST['image1'] 
    image2 = 'images/' + request.POST['image2']
    prix_u = request.POST['prix_u']
    quantite = request.POST['quantite']
    description = request.POST['description']
    libelle_categorie = request.POST['categorie']
    categorie = Categorie.objects.get(libelle = libelle_categorie)
    try:
        produit = Produit.objects.create(libelle=libelle, prix_u=prix_u, quantite=quantite, 
        description=description, categorie=categorie, image1 = image1, image2 = image2, 
        fournisseur = detail_devis.devis.fournisseur )
    except KeyError:
        error = "l'une des clés est invalide"
        return render(request, 'produit/create_produit.html', {'error': error})
    try:
        DetailDevis.objects.filter(id = id_detail_devis).update(ajouter = 1)
    except:
        error = "Erreur l'hors du mise à jour du détail devis"
        return render(request, 'produit/create_produit.html', {'error': error})
    else:
        return HttpResponseRedirect('/gestion_produit/categorie/' + str(produit.categorie.id) )

def delete_produit(request, id_produit):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' ) 
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_p":
        return HttpResponseRedirect('/' )  
    produit_deleted = Produit.objects.get(id = id_produit)
    categorie = produit_deleted.categorie
    produit_deleted.delete()
    return HttpResponseRedirect('/gestion_produit/categorie/' + str(categorie.id) )

def edit_produit(request, id_produit):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )  
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_p":
        return HttpResponseRedirect('/' ) 
     # verifier si des produits sont disponibles en stock
    try:
        devis = Devis.objects.get(etat = 1)
        all_detail_devis = DetailDevis.objects.filter(ajouter = 0, devis = devis.first())
    except:
        all_detail_devis = []
        detail_devis = DetailDevis.objects.filter(ajouter = 0)
        for detail in detail_devis:
            if detail.devis.etat == 1:
                all_detail_devis.append(detail)   
    produit_edited = Produit.objects.get(id = id_produit)
    categories = Categorie.objects.all()
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'produit/edit_produit.html', 
    {'produit_edited': produit_edited, 
        'employe_login': employe_login,
    'messages': messages,
    'categories': categories, 'all_detail_devis': all_detail_devis})

def save_edit_produit(request, id_produit):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_p":
        return HttpResponseRedirect('/' ) 
    produit_edited = Produit.objects.get(id = id_produit)
    libelle = request.POST['libelle']
    prix_u = request.POST['prix_u']
    quantite = request.POST['quantite']
    description = request.POST['description']
    libelle_categorie = request.POST['categorie']
    image1 = request.POST['imageun']
    image2 = request.POST['imagedeux']
    if image1 != '':
        image1 = 'images/' + str(image1)
    else:
        image1 = produit_edited.image1
    if image2 != '':
        image2 = 'images/' + str(image2)
    else:
        image2 = produit_edited.image2
    categorie = Categorie.objects.get(libelle = libelle_categorie)
    Produit.objects.filter(id = id_produit).update( libelle = libelle, prix_u = prix_u, 
                                                quantite = quantite, description = description, 
                                                categorie = categorie, image1 = image1, image2 = image2 )
    return HttpResponseRedirect('/gestion_produit/categorie/' + str(categorie.id) )





     
