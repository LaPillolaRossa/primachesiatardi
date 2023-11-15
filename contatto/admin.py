from django.contrib import admin
from .models import BlacklistIP, ModelloContatto
BlacklistIP

# Register your models here.

class ContattoModelAdmin(admin.ModelAdmin):
    model = ModelloContatto
    list_display = ["email", "oggetto", "file", "ip", "user_agent", "host_name", "data_creazione"]
    search_fields = ["nome", "cognome", "email", "oggetto"]
    list_filter = ["oggetto", "email"]
    

admin.site.register(ModelloContatto, ContattoModelAdmin)
admin.site.register(BlacklistIP)