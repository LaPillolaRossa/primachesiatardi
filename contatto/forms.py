from django import forms
from .models import ModelloContatto


class FormModelloContatto(forms.ModelForm):
    
    class Meta:
        model = ModelloContatto
        fields = "__all__"
        widgets = {"contenuto": forms.Textarea(attrs={"placeholder": "Scrivi qui il contenuto del tuo messaggio..."})}
        labels = {"nome": "Nome", "cognome": "Cognome", "email": "Email", "oggetto": "Oggetto", "contenuto": "Messaggio"}
        
        
        #widgets = {"nome": forms.CharField(attrs={"placeholder": "Nome"}),
        #           "cognome": forms.CharField(attrs={"placeholder": "Cognome"}),
        #           "email": forms.EmailField(attrs={"placeholder": "Email"}),
        #           "oggetto": forms.CharField(attrs={"placeholder": "Oggetto del messaggio"}),
        #           "contenuto": forms.Textarea(attrs={"placeholder": "Scrivi qui il contenuto del tuo messaggio..."})}