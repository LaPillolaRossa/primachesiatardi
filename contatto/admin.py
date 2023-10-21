from django.contrib import admin
from .models import ModelloContatto

# Register your models here.

class ContattoModelAdmin(admin.ModelAdmin):
    model = ModelloContatto
    list_display = ["email", "oggetto", "file"]
    search_fields = ["nome", "cognome", "email", "oggetto"]
    list_filter = ["oggetto", "email"]
    

admin.site.register(ModelloContatto, ContattoModelAdmin)