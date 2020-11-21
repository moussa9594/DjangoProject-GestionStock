from django.shortcuts import render
from .forms import EmployeForm, MessageForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Employe, Message
# Create your views here.
def employe(request):
    form = EmployeForm()
    return render(request, 'employe/employe.html', {'form': form})

def message(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/') 
    id_employe = request.session.get('id_employe')
    employe = Employe.objects.get(id = id_employe)
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/')  
    return render(request, 'employe/message.html',
     {'form': MessageForm(),
      'employe': employe
     })

def save_message(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/')  
    # message = MessageForm(request.POST)
    id_employe = request.session.get('id_employe')
    employe = Employe.objects.get(id = id_employe)
    # new_message = message.save()
    text = request.POST["text"]
    objet = request.POST["objet"]
    email_destinataire = request.POST["destinataire"]
    error = ""
    try:
        destinataire = Employe.objects.get(email = email_destinataire)
        message = Message.objects.create(employe = employe, destinataire = email_destinataire, objet = objet, text = text)
        if employe.role == 'g_p':
            return HttpResponseRedirect('/gestion_produit/categorie/3' ) 
        elif employe.role == 'g_c':
            return HttpResponseRedirect('/gestion_commande') 
        else:
            return HttpResponseRedirect('/gestion_fournisseur')
    except:
        error = "Ce mail n'existe pas"
        return render(request, 'employe/message.html',
        {
         'form': MessageForm(),
         'employe': employe,
         'error': error,
        })

def get_messages(request):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    mes_messages = Message.objects.filter( destinataire = employe_login.email).order_by('date')
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'employe/boite_reception.html', {
        'mes_messages': mes_messages,
        'messages': messages,
        'employe': employe_login
    })

def reponse_message(request, id_message):
    if request.session.get('id_employe') == None:
        return HttpResponseRedirect('/' )    
    message = Message.objects.get(id = id_message)
    Message.objects.filter(id = id_message).update( lire = 1 )
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    messages = Message.objects.filter( destinataire = employe_login.email, lire = 0)
    return render(request, 'employe/reponse_message.html', {
        'message': message,
        'messages': messages,
        'employe': employe_login
    })
