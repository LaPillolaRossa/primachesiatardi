from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

from .forms import ArticoloModelForm, CommentoModelForm
from .mixins import StaffMixing
from .models import Articolo, Commento, Sezione


# Create your views here.

    
def visualizza_sezione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
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
    likes_connected = get_object_or_404(Articolo, slug=slug)
    numero_di_like_articolo = likes_connected.get_total_like_articolo()
    like_articolo = False
    if likes_connected.like_articolo.filter(id=request.user.id).exists():
        like_articolo = True
    
    paginator = Paginator(commenti_articolo, 10)
    page = request.GET.get("pagina")
    commenti = paginator.get_page(page)
    
    form_risposta = CommentoModelForm()
    context = {"articolo": articolo, "articolo_è_piaciuto": like_articolo, "numero_di_like_articolo": numero_di_like_articolo, "commenti": commenti, "commenti_articolo": commenti_articolo, "form_risposta": form_risposta}
    return render(request, "news/singolo_articolo.html", context)

    

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

    
@staff_required(login_url="/accounts/login")
def crea_articolo(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    if request.method == "POST":
        form = ArticoloModelForm(request.POST)
        if form.is_valid():
            articolo = form.save(commit=False) # Si sospende temporaneamente la creazione dell'oggetto per aggiungere attributi aggiuntivi
            articolo.sezione_appartenenza = sezione
            articolo.autore_articolo = request.user
            articolo.save()
            return HttpResponseRedirect(articolo.get_absolute_url()) 
    else:
        form = ArticoloModelForm()
    context = {"form": form, "sezione": sezione}
    return render(request, "news/crea_articolo.html", context)


class AggiornaArticolo(StaffMixing, UpdateView):
    model = Articolo
    template_name = "news/aggiorna_articolo.html"
    fields = ['titolo', 'contenuto', 'immagine', "autore_articolo", "sezione_appartenenza", "slug"]
    
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
#    paginate_by = 5
        

#    def get_context_data(self, **kwargs):
#        context = super(VisualizzaArticolo, self).get_context_data(**kwargs)
        
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
#        articolo = get_object_or_404(Articolo, pk=self.kwargs['pk'])
#        queryset = Commento.objects.filter(articolo=articolo) 
#        paginator = Paginator(queryset, 5) #paginate_by
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





    
