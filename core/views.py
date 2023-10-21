from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from news.models import Articolo, Commento, Sezione
import random
# Create your views here.

    
def homepageview(request):
    articoli = list(Articolo.objects.all())
    random_articoli = random.sample(articoli, 2)
    sezioni = Sezione.objects.all()
    lista_articoli = Articolo.objects.all()
    ultimi_articoli = Articolo.objects.filter().order_by("-pk")
    archivio_2009 = Articolo.objects.filter(data_creazione__year = 2009)
    archivio_2010 = Articolo.objects.filter(data_creazione__year = 2010)
    archivio_2011 = Articolo.objects.filter(data_creazione__year = 2011)
    archivio_2012 = Articolo.objects.filter(data_creazione__year = 2012)
    archivio_2013 = Articolo.objects.filter(data_creazione__year = 2013)
    archivio_2014 = Articolo.objects.filter(data_creazione__year = 2014)
    context = {"lista_articoli": lista_articoli, 
               "sezioni": sezioni, 
               "ultimi_articoli": ultimi_articoli,
               "random_articoli": random_articoli, 
               "archivio_2009": archivio_2009, 
               "archivio_2010": archivio_2010, 
               "archivio_2011": archivio_2011, 
               "archivio_2012": archivio_2012, 
               "archivio_2013": archivio_2013, 
               "archivio_2014": archivio_2014
    }
    return render(request, "core/homepage.html", context)

def manifesto_view(request):
    return render(request, "core/manifesto.html")
    
def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    articoli_utente = Articolo.objects.filter(autore_articolo=user).order_by("-pk")
    commenti_utente = Commento.objects.filter(autore_commento=user).order_by("-pk")
    context = {"user": user, "articoli_utente": articoli_utente, "commenti_utente": commenti_utente}
    return render(request, "core/user_profile.html", context)

def cerca(request):
    if "q" in request.GET:
        querystring = request.GET.get("q")
        if len(querystring) == 0:
            return redirect("/cerca/")
        articoli = Articolo.objects.filter(titolo__icontains=querystring)
        commenti = Commento.objects.filter(contenuto__icontains=querystring)
        users = User.objects.filter(username__icontains=querystring)
        context = {"articoli": articoli, "commenti": commenti, "users": users}
        return render(request, "core/cerca.html", context)
    else:
        return render(request, "core/cerca.html")
    

