import logging

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.utils.html import strip_tags
from .forms import ArticoloModelForm, CommentoModelForm
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from .mixins import StaffMixing
from .models import Articolo, Commento, Sezione

import requests

logger = logging.getLogger(__name__)

# Create your views here.
    
    
def visualizza_sezione(request, slug):
    sezione = get_object_or_404(Sezione, slug=slug)
    articoli_sezione = Articolo.objects.filter(sezione_appartenenza=sezione).order_by("-data_creazione")
    context = {"sezione": sezione, "articoli": articoli_sezione}
    return render(request, "news/singola_sezione.html", context)
    

class CreaSezione(StaffMixing, CreateView):
    model = Sezione
    fields = "__all__"
    template_name = "news/crea_sezione.html"
    success_url = "/"


def visualizza_articolo(request, slug):
    articolo = get_object_or_404(Articolo, slug=slug)
    commenti_articolo = Commento.objects.filter(articolo=articolo)
    articoli = Articolo.objects.all()

    likes_connected = get_object_or_404(Articolo, slug=slug)
    numero_di_like_articolo = likes_connected.get_total_like_articolo()
    like_articolo = False
    if likes_connected.like_articolo.filter(id=request.user.id).exists():
        like_articolo = True
    
    paginator = Paginator(commenti_articolo, 10)
    page = request.GET.get("pagina")
    commenti = paginator.get_page(page)
    
    form_risposta = CommentoModelForm()
    context = {
        "articolo": articolo, 
        "articolo_è_piaciuto": like_articolo, 
        "numero_di_like_articolo": numero_di_like_articolo, 
        "commenti": commenti, 
        "commenti_articolo": commenti_articolo, 
        "form_risposta": form_risposta,
        "articoli": articoli, 
    }
    
    hit_count = get_hitcount_model().objects.get_for_object(articolo)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    
    return render(request, "news/singolo_articolo.html", context)

    

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)



class AggiornaArticolo(StaffMixing, UpdateView):
    model = Articolo
    template_name = "news/aggiorna_articolo.html"
    fields = ['titolo', "descrizione", "contenuto", "immagine", "autore_articolo", "sezione_appartenenza", "slug"]
    
    def get_success_url(self):
        articolo = self.object
        return reverse("visualizza_articolo", kwargs={"slug": articolo.slug})
    
class CancellaArticolo(StaffMixing, DeleteView):
    model = Articolo
    
    def get_success_url(self):
        return reverse("homepage")
    

@login_required
def aggiungi_commento(request, slug):
    articolo = get_object_or_404(Articolo, slug=slug)
    if request.method == "POST":
        form = CommentoModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.articolo = articolo
            form.instance.autore_commento = request.user
            form.save()
            
            url_articolo = reverse("visualizza_articolo", kwargs={"slug": slug})
            pagine_in_articolo = articolo.get_n_pages()
            if pagine_in_articolo > 1:
                success_url = url_articolo + "?pagina=" + str(pagine_in_articolo)               
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(url_articolo)
        
    else:
        return HttpResponseBadRequest
    

class CancellaCommento(DeleteView):
    model = Commento 

    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(autore_commento_id=self.request.user.id)
    
    def get_success_url(self):
        articolo = self.object.articolo
        return reverse("visualizza_articolo", kwargs={"slug": articolo.slug})
    
      
def aggiungi_like_articolo(request, slug):
    articolo = get_object_or_404(Articolo, slug=slug)
    url_articolo = reverse("visualizza_articolo", kwargs={"slug": slug})
    if articolo.like_articolo.filter(id=request.user.id).exists():
        articolo.like_articolo.remove(request.user)
    else:
        articolo.like_articolo.add(request.user)

    return HttpResponseRedirect(url_articolo)




#class VisualizzaArticolo(DetailView):
#    model = Articolo
#    fields = "__all__"
#    template_name = "news/singolo_articolo.html"
#    paginate_by = 10
        

#    def get_context_data(self, **kwargs):
#        context = super(VisualizzaArticolo, self).get_context_data(**kwargs)
#        
#        articolo = get_object_or_404(Articolo, pk=self.kwargs['pk'])        
#        commenti_articolo = Commento.objects.filter(articolo=articolo)
#        form_risposta = CommentoModelForm()
#        likes_connected = get_object_or_404(Articolo, id=self.kwargs['pk'])
#        like_articolo = False
#        if likes_connected.like_articolo.filter(id=self.request.user.id).exists():
#            like_articolo = True
            
#        context['articolo'] = articolo 
#        context['form_risposta'] = form_risposta
#        context['articolo_è_piaciuto'] = like_articolo
#        context['numero_di_like_articolo'] = likes_connected.get_total_like_articolo()
#        context['commenti_articolo'] = commenti_articolo
        
#        return context
    
#    def get_pagination(self):
#        articolo = get_object_or_404(Articolo, slug=self.kwargs['slug'])
#        queryset = Commento.objects.filter(articolo=articolo) 
#        paginator = Paginator(queryset, 10) #paginate_by
#        page = self.request.GET.get('pagina')
#        commenti_articolo = paginator.get_page(page)
#        return commenti_articolo


#class CreaArticolo(StaffMixing, CreateView):
#    model = Articolo
#    template_name = "news/crea_articolo.html"
#    fields = ['titolo', 'contenuto', 'immagine', 'autore_articolo', 'sezione_appartenenza']
    
#    def get_context_data(self, **kwargs):
#        context = super(CreaArticolo, self).get_context_data(**kwargs)
#        pk = self.pk
#        request=self.request
#        sezione = get_object_or_404(Sezione, pk=pk)
#        if request.method == "POST":
#            form = ArticoloModelForm(request.POST)
#            if form.is_valid():
#                articolo = form.save(commit=False) 
#                articolo.sezione_appartenenza = sezione
#                articolo.autore_articolo = request.user
#                articolo.save()
#                return HttpResponseRedirect(articolo.get_absolute_url()) 
#        else:
#            form = ArticoloModelForm()
#        context['form'] = form
#        context['sezione'] = sezione
        
#    def get_form(self):
#        form = ArticoloModelForm()
#        return form(**self.get_form())



#def aggiungi_like_commento(request, pk):
#    articolo = get_object_or_404(Articolo, pk=pk)
#    commento = Commento.objects.filter(articolo=articolo)
#    url_articolo = reverse("visualizza_articolo", kwargs={"pk": pk})
#    if commento.like_commento.filter(id=request.user.id).exists():
#        commento.like_commento.remove(request.user)
#    else:
#        commento.like_commento.add(request.user)
#
#    return HttpResponseRedirect(url_articolo)



def invio_articolo_su_telegram(titolo_articolo, url_articolo, contenuto, immagine_url):
    """Pubblica l'articolo sul canale Telegram. Un errore di Telegram non blocca la creazione dell'articolo."""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not bot_token or not chat_id:
        return None

    # Testo semplice: con MarkdownV2 ogni punto o trattino andrebbe preceduto da "\"
    messaggio = f"{titolo_articolo}\n{url_articolo}\n\n{contenuto}"
    api = f'https://api.telegram.org/bot{bot_token}'

    try:
        if immagine_url:
            # La didascalia di una foto può avere al massimo 1024 caratteri
            response = requests.post(f'{api}/sendPhoto', data={
                'chat_id': chat_id,
                'photo': immagine_url,
                'caption': messaggio[:1024],
            }, timeout=10)
        else:
            # Un messaggio di testo può avere al massimo 4096 caratteri
            response = requests.post(f'{api}/sendMessage', data={
                'chat_id': chat_id,
                'text': messaggio[:4096],
            }, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        logger.exception("Invio dell'articolo su Telegram non riuscito")
        return None




@staff_required(login_url="/accounts/login")
def crea_articolo(request):
    if request.method == "POST":
        form = ArticoloModelForm(request.POST, request.FILES)  # Aggiungi request.FILES per il campo immagine
        if form.is_valid():
            # Salva l'articolo senza commettere immediatamente per aggiungere il valore autore
            articolo = form.save(commit=False)
            articolo.autore_articolo = request.user
            articolo.save()  # Ora salva l'articolo nel database

            # Dopo aver salvato l'articolo, invia il messaggio su Telegram.
            # Telegram ha bisogno di URL completi, con il dominio, per aprire il link e scaricare l'immagine.
            url_articolo = request.build_absolute_uri(articolo.get_absolute_url())
            contenuto = strip_tags(articolo.contenuto)  # il contenuto arriva da CKEditor in HTML

            immagine_url = None
            if articolo.immagine:
                immagine_url = request.build_absolute_uri(articolo.immagine.url)

            # Invia il messaggio su Telegram (titolo, contenuto, URL e immagine se presente)
            invio_articolo_su_telegram(articolo.titolo, url_articolo, contenuto, immagine_url)

            # Redirigi all'articolo appena creato
            return HttpResponseRedirect(articolo.get_absolute_url())
    else:
        form = ArticoloModelForm()

    context = {"form": form}
    return render(request, "news/crea_articolo.html", context)
