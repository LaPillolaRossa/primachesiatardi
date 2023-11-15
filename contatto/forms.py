from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from .models import ModelloContatto


class FormModelloContatto(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    
    class Meta:
        model = ModelloContatto
        fields = "__all__"
        widgets = {
            "nome": forms.Textarea(attrs={"placeholder": "Scrivi qui il tuo nome..", 'rows': '1'}),
            "cognome": forms.Textarea(attrs={"placeholder": "Scrivi qui il tuo cognome..", 'rows': '1'}),
            "email": forms.Textarea(attrs={"placeholder": "Scrivi qui la tua mail..", 'rows': '1'}),
            "oggetto": forms.Textarea(attrs={"placeholder": "Scrivi qui il contenuto dell'oggetto..", 'rows': '1'}),
            "contenuto": forms.Textarea(attrs={"placeholder": "Scrivi qui il contenuto del tuo messaggio...", 'rows': '5'}),
                   
        }
        labels = {
            "nome": "Nome:", 
            "cognome": "Cognome:", 
            "email": "Email:", 
            "oggetto": "Oggetto:", 
            "contenuto": "Messaggio:",
            "file": "File:",
        }
        
