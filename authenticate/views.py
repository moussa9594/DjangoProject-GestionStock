from django.shortcuts import render
from employe.models import Employe
from .forms import LoginForm
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

# affichage de la page de conexion
def index(request):
    return render(request, 'authenticate/index.html', 
    {'form': LoginForm(),
     'change_password': 'oui'})

# verification du login et du mdp
def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        try:
            employe = Employe.objects.get(email = email, password = password)
        except Employe.DoesNotExist:
            login_failed = "Login ou mot de passe incorrect."
            return render(request, 'authenticate/index.html', 
            {'login_failed': login_failed, 'form': LoginForm(), 'change_password': 'oui'})
        else:
            employe = Employe.objects.get(email = email)
            request.session['id_employe'] = employe.id
            if password == 'passer':
                    return render(request, 'authenticate/index.html', 
                    {'change_password': 'non'})
            if employe.role == 'g_p':
                return HttpResponseRedirect('/gestion_produit/categorie/3' ) 
            elif employe.role == 'g_c':
                return HttpResponseRedirect('/gestion_commande') 
            else:
                return HttpResponseRedirect('/gestion_fournisseur') 
    else:
        login_failed = "Champs invalid."
        return render(request, 'authenticate/index.html', {'login_failed': login_failed, 'form': LoginForm()})

def logout(request):
    try:
        del request.session['id_employe']
    except KeyError:
        pass
    return render(request, 'authenticate/index.html',
     {'form': LoginForm(), 'change_password': 'oui'})

def change_pwd(request):
    pwd1 = request.POST['pwd1']
    pwd2 = request.POST['pwd2']
    if pwd1 != pwd2:
        return render(request, 'authenticate/index.html',
         {'pwd1_Eq_pwd2': 'non', 'change_password': 'non' })
    elif pwd1 == pwd2 and pwd1 == 'passer':
        return render(request, 'authenticate/index.html',
         {'pwd1_Eq_pwd2_Eq_passer': 'oui', 'change_password': 'non' })
    else:
        id_employe = int(request.session['id_employe'])
        try:
            Employe.objects.filter(id = id_employe).update(password = pwd1)
            employe = Employe.objects.get(id = id_employe)
            if employe.role == 'g_p':
                return HttpResponseRedirect('/gestion_produit/categorie/3' ) 
            elif employe.role == 'g_c':
                return HttpResponseRedirect('/gestion_commande') 
            else:
                return HttpResponseRedirect('/gestion_fournisseur') 
        except:
            return render(request, 'authenticate/index.html',
         { 'change_password': 'non' })
        