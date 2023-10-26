from calendario.models import Events 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse 
from django.utils import timezone

# Create your views here.

now = timezone.now()


@login_required
def calendario(request):
    all_events = Events.objects.all()
    context = {"events": all_events}
    return render(request, "calendario/calendario.html", context)

@login_required
def all_events(request):
    all_events = Events.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
            })
    return JsonResponse(out, safe=False)

@login_required
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title =request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)

@login_required
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title =request.GET.get("title", None)
    id =request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)

@login_required
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

