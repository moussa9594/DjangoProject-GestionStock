from django.shortcuts import render
from .models import Fournisseur, Devis, DetailDevis
from .forms import FournisseurForm
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
import datetime
from django.core.mail import send_mail
from django.conf import settings
from employe.models import Employe, Message


from django.core.cache import cache

# Create your views here.
def fournisseur(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )  
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' ) 
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/index.html', {
        'fournisseurs': Fournisseur.objects.all(),
        'messages': messages,
        'employe_login': employe_login
    })
    

def create_fournisseur(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' ) 
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/create_fournisseur.html', 
    {
        'messages': messages,
        'form': FournisseurForm(),
        'employe_login': employe_login
    })

def save_fournisseur(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' ) 
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' )    
    # init fournisseur
    fournisseur = ''
    prenom = request.POST['prenom']
    nom = request.POST['nom']
    telephone = request.POST['telephone']
    email = request.POST['email']
    sexe = request.POST['sexe']
    adresse = request.POST['adresse']
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    try:
        fournisseur = Fournisseur.objects.create(prenom=prenom, nom=nom, telephone=telephone, 
                                                  email=email, sexe=sexe, adresse=adresse)
    except KeyError:
        error = "l'une des clés est invalide"
        return render(request, 'fournisseur/create_fournisseur.html', {'error': error,
        'messages': messages,
        'employe_login': employe_login})
    else:
        return HttpResponseRedirect('/gestion_fournisseur' )

def detail_fournisseur(request, id_fournisseur):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' ) 
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' )    
    fournisseur = Fournisseur.objects.get(id = id_fournisseur)
    request.session['id_fournisseur'] = fournisseur.id
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/detail.html', {
        'messages': messages,
        'fournisseur': fournisseur,
        'employe_login': employe_login
    })

def demande(request, id_fournisseur):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )  
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' )   
    fournisseur = Fournisseur.objects.get(id = id_fournisseur)
    request.session['fournisseur_id'] = fournisseur.id
    #Ajout dans la table devis
    devis = Devis.objects.get_or_create(date_devis = datetime.date.today(), fournisseur = fournisseur)
    devis2 = Devis.objects.get(date_devis = datetime.date.today(), fournisseur = fournisseur)
    all_detail_devis = DetailDevis.objects.all().filter(devis = devis2, ajouter = 0)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/demande.html', {
        'messages': messages,
        'fournisseur': fournisseur,
        'all_detail_devis': all_detail_devis,
        'employe_login': employe_login
    })

def add_demande(request):
            if request.session.get('id_employe') == None:
                return HttpResponseRedirect('/' ) 
            id_employe = request.session.get('id_employe')
            employe_login = Employe.objects.get(id = id_employe)
            if employe_login.role != "g_f":
                return HttpResponseRedirect('/' )    
            id_fournisseur = int(request.session['fournisseur_id'])
            fournisseur = Fournisseur.objects.get(id = id_fournisseur)
            devis = Devis.objects.get(date_devis = datetime.date.today(), fournisseur = fournisseur)
        # try :
            libelle = request.POST["libelle"]
            quantite = request.POST["quantite"]
            if libelle != '' and quantite != '':
                #vérifier s'il n'a pas déja ajouter le même
                try:
                    detail_devis = DetailDevis.objects.get(devis = devis, libelle = libelle)
                    if detail_devis :
                        qt = int(quantite) + detail_devis.quantite
                        DetailDevis.objects.filter(devis = devis, libelle = libelle).update(quantite = qt)
                    else:
                        #Ajout dans la table detail_devis
                        detail_devis = DetailDevis.objects.create(libelle = libelle, quantite = quantite, devis = devis)
                except:
                        detail_devis = DetailDevis.objects.create(libelle = libelle, quantite = quantite, devis = devis)

        #modification du nbre de produit dans devis
            all_detail_devis = DetailDevis.objects.filter(devis = devis, ajouter =0)
            count = len(all_detail_devis)
            devis = Devis.objects.filter(date_devis = datetime.date.today(), fournisseur = fournisseur).update(nbre_produit = count)
            messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
            return render(request, 'fournisseur/demande.html', {
        'messages': messages,
        'fournisseur': fournisseur,
        'all_detail_devis': all_detail_devis,
        'count': count,
        'employe_login': employe_login
        })
        # except :
        #     none_devis = "Aucun devis n'a été enregistrer"
        #     return render(request, 'fournisseur/demande.html', {
        # 'fournisseur': fournisseur,
        # 'none_devis': none_devis,
        
        # })



def sendmail(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )  
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' )   
#     send_mail('This is the title of the email',
#           'This is the message you want to send',
#           settings.EMAIL_HOST_USER,
#           [
#               'thiernodiallo2505@gmail.com', # add more emails to this list of you want to
#           ],
#           fail_silently=False,
# )
    mes_devis = []
    id_fournisseur = int(request.session['fournisseur_id'])
    fournisseur = Fournisseur.objects.get(id = id_fournisseur)
    # devis = Devis.objects.filter( date_devis = datetime.date.today(), fournisseur = fournisseur )
    devis = Devis.objects.all()
    detail_devis = DetailDevis.objects.filter(ajouter = 0)
    for dd in detail_devis:
        for d in devis:
            if dd.devis == d:
                mes_devis.append(d)
                
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/approuver_demande.html', {
        'messages': messages,
        'devis': set(mes_devis),
        'employe_login': employe_login
    })

def approuver_demande(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' )     
    devis = Devis.objects.filter( etat = 0).exclude(nbre_produit = 0)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/approuver_demande.html', {
        'messages': messages,
        'devis': devis,
        'employe_login': employe_login
    })

def valider_devis(request, id_devis):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' )     
    devis = Devis.objects.get( id = id_devis)
    detail_devis = DetailDevis.objects.filter(devis = devis, ajouter = 0)
    fournisseur = devis.fournisseur
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/approuver_demande.html', {
        'messages': messages,
        'detail_devis': detail_devis,
        'my_devis': devis,
        'fournisseur': fournisseur,
        'employe_login': employe_login
    })

def change_etat_devis(request, id_devis):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' ) 
    Devis.objects.filter( id = id_devis).update(etat = 1)
    devis = Devis.objects.filter( etat = 0)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/approuver_demande.html', {
        'messages': messages,
        'devis': devis,
        'employe_login': employe_login
    })

def historique(request, id_fournisseur):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' ) 
    fournisseur = Fournisseur.objects.get(id = id_fournisseur)
    devis = Devis.objects.filter(fournisseur = fournisseur)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/historique.html', {
        'messages': messages,
        'fournisseur': fournisseur,
        'devis': devis,
        'employe_login': employe_login
    })

def voir_devis(request, id_devis):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' ) 
    devis = Devis.objects.filter( etat = 0)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/approuver_demande.html', {
        'messages': messages,
        'devis': devis,
        'employe_login': employe_login
    })

def delete_devis(request, id_devis):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_f":
        return HttpResponseRedirect('/' ) 
    Devis.objects.get(id = id_devis).delete()
    devis = Devis.objects.filter( etat = 0)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'fournisseur/approuver_demande.html', {
        'messages': messages,
        'devis': devis,
        'employe_login': employe_login
    })


