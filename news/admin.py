from django.contrib import admin
from .models import Articolo, Commento, Sezione


# Register your models here.

class ArticoloModelAdmin(admin.ModelAdmin):
    model = Articolo
    list_display = ["titolo", "sezione_appartenenza", "autore_articolo"]
    search_fields = ["titolo", "autore_articolo__username"]
    list_filter = ["sezione_appartenenza", "data_creazione"]
    
class CommentoModelAdmin(admin.ModelAdmin):
    model = Commento
    list_display = ["autore_commento", "articolo"]
    search_fields = ["contenuto",]
    list_filter = ["data_creazione", "autore_commento"]
    
class SezioneModelAdmin(admin.ModelAdmin):
    model = Sezione
    list_display = ["nome_sezione", "descrizione"]
    


admin.site.register(Articolo, ArticoloModelAdmin)
admin.site.register(Commento, CommentoModelAdmin)
admin.site.register(Sezione, SezioneModelAdmin)

