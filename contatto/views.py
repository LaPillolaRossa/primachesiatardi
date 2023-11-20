from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import FormModelloContatto
from .models import BlacklistIP, ModelloContatto
from django.core.mail import EmailMessage
from smtplib import SMTPRecipientsRefused

# Create your views here.

def contatti(request):
    
    if request.method == "POST":
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        user_agent = request.headers.get('User-Agent', '')[:255]
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        if BlacklistIP.objects.filter(ip__exact=ip):
            return HttpResponse("<h1>Internal server error (500)<h1>")
        form = FormModelloContatto(request.POST, request.FILES)
        if request.POST.get('file', True):
            ModelloContatto(file=request.FILES["file"])
        if form.is_valid():
            try:            
                destinatario = form.cleaned_data["email"]            
                email = EmailMessage(
                    "Richiesta di collaborazione",
                    """Ti ringraziamo per averci contattato. Visioneremo la tua proposta e ti contatteremo entro un massimo di 48 ore.""",
                    "comunicazioni@primachesiatardi.com",
                    [destinatario],
                    headers={"Message-ID": "foo"},
                )
                email.send()
            
            except SMTPRecipientsRefused:
                html = "<html><body><div>Attenzione!! Hai inserito un'email non valida! Clicca il link sottostante per ricompilare il form:</div><div><a href='/contattaci'>Contattaci</a></div></body></html>"
                return HttpResponse(html)
            
            instance = form.save(commit=False)
            instance.ip = ip
            instance.user_agent = user_agent   
            instance.save()          

            email_avviso = EmailMessage(
                "Richiesta di collaborazione",
                """Un utente ha inviato una richiesta di collaborazione. Puoi visionarne i dettagli all'interno dell'area amministrativa del sito. Di seguito il link per accedervi: https://www.primachesiatardi.com/admin/""",
                "comunicazioni@primachesiatardi.com",
                ["destinatario@example.com", "destinatario@example.com"],
                headers={"Message-ID": "foo"},
            )
            email_avviso.send()              
            return redirect("/contattaci-successo")
    else:
        form = FormModelloContatto()

    context = {"form": form}
    return render(request, "contatto/contatto.html", context)


def contatto_done(request):
    return render(request, "contatto/contatto_done.html")
    






