from django.shortcuts import redirect, render
from .forms import FormModelloContatto
from .models import ModelloContatto
from django.core.mail import EmailMessage


# Create your views here.

def contatti(request):
    
    if request.method == "POST":
        form = FormModelloContatto(request.POST, request.FILES)
        file = request.POST.get('file', True)
        if file:
            if form.is_valid():
                form.cleaned_data["nome"]
                form.cleaned_data["cognome"]
                form.cleaned_data["email"]
                form.cleaned_data["oggetto"]
                form.cleaned_data["contenuto"]
                file = ModelloContatto(file=request.FILES["file"])
                form.save()    
                destinatario = form.cleaned_data["email"]            
                email = EmailMessage(
                    "Richiesta di collaborazione",
                    """Ti ringraziamo per averci contattato. Visioneremo la tua proposta e ti contatteremo entro un massimo di 48 ore.""",
                    "destinatario@example.com",
                    [destinatario],

                    headers={"Message-ID": "foo"},
                )
                email.send()              
                return redirect("/contattaci-successo")
                 
        else:
            form = FormModelloContatto(request.POST)
            if form.is_valid():
                form.cleaned_data["nome"]
                form.cleaned_data["cognome"]
                form.cleaned_data["email"]
                form.cleaned_data["oggetto"]
                form.cleaned_data["contenuto"]
                form.save()
                destinatario = form.cleaned_data["email"]
                email = EmailMessage(
                    "Richiesta di collaborazione",
                    """Ti ringraziamo per averci contattato. Visioneremo la tua proposta e ti contatteremo entro un massimo di 48 ore.""",
                    "destinatario@example.com",
                    [destinatario],
                    headers={"Message-ID": "foo"},
                )
                email.send()
                return redirect("/contattaci-successo")
    else:
        form = FormModelloContatto()

    context = {"form": form}
    return render(request, "contatto/contatto.html", context)


def contatto_done(request):
    return render(request, "contatto/contatto_done.html")
    






