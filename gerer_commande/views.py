from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from employe.models import Employe
from gestion_commande.models import Commande
# Create your views here.

def commandes(request):
    if 'id_employe' not in request.session:
            return HttpResponseRedirect('/' )
    id_employe = request.session.get('id_employe')
    employe_login = Employe.objects.get(id = id_employe)
    if employe_login.role != "g_c":
        return HttpResponseRedirect('/' ) 
    commandes = Commande.objects.filter(etat = 0)
    return render(request, 'gerer_cde/index.html', {
        'employe_login': employe_login,
        'commandes': commandes
    })