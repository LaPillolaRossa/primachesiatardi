from django import forms
from .models import ModelloContatto


class FormModelloContatto(forms.ModelForm):
    
    class Meta:
        model = ModelloContatto
        fields = "__all__"
        widgets = {"contenuto": forms.Textarea(attrs={"placeholder": "Scrivi qui il contenuto del tuo messaggio...", 'rows': '5'})}
        labels = {"nome": "Nome", "cognome": "Cognome", "email": "Email", "oggetto": "Oggetto", "contenuto": "Messaggio"}
        
