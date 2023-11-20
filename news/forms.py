from django import forms
from .models import Articolo, Commento


class ArticoloModelForm(forms.ModelForm):

    class Meta:
        model = Articolo
        fields = ["titolo", "descrizione", "contenuto", "immagine", 'autore_articolo', 'sezione_appartenenza','slug']
        widgets = {"titolo": forms.TextInput(attrs={"placeholder": "Titolo dell'Articolo"})}
        labels = {"contenuto" : ""}
        
                       
class CommentoModelForm(forms.ModelForm):
    
    class Meta:
        model = Commento
        fields = ["contenuto"]
        widgets = {"contenuto": forms.Textarea(attrs={'rows': '5'})}
        labels = {"contenuto": "Messaggio"}