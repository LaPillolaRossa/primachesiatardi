from django.urls import path

from . import views

urlpatterns = [
    
    path('contattaci/', views.contatti, name="contattaci"),
    path('contattaci-successo/', views.contatto_done, name="contattaci_successo"),
]