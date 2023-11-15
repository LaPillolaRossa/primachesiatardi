from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import FormModelloContatto
from .models import BlacklistIP, ModelloContatto
from django.core.mail import EmailMessage



# Create your views here.

def contatti(request):
    
    if request.method == "POST":
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        user_agent = request.headers.get('User-Agent', '')[:255]
        host_name = request.META.get('REMOTE_HOST')
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
                        
            instance = form.save(commit=False)
            instance.ip = ip
            instance.user_agent = user_agent
            instance.host_name = host_name   
            instance.save()
                        
            destinatario = form.cleaned_data["email"]            
            email = EmailMessage(
                "Richiesta di collaborazione",
                """Ti ringraziamo per averci contattato. Visioneremo la tua proposta e ti contatteremo entro un massimo di 48 ore.""",
                "comunicazioni@primachesiatardi.com",
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
    






