from django.urls import path
from . import views

urlpatterns = [
    path('nuova-sezione/', views.CreaSezione.as_view(), name="crea_sezione"),
    path('sezione/<int:pk>/', views.visualizza_sezione, name="sezione_view"),
    path('sezione/<int:pk>/crea-articolo', views.crea_articolo, name="crea_articolo"),
    path('articolo/<str:slug>/', views.visualizza_articolo, name="visualizza_articolo"),
    path('mi-piace-articolo/<str:slug>/', views.aggiungi_like_articolo, name="aggiungi_mipiace_articolo"),
    path('articolo/<str:slug>/rispondi/', views.aggiungi_commento, name="rispondi_ad_articolo"),
    path('articolo/<int:id>/elimina-commento/<int:pk>/', views.CancellaCommento.as_view(), name="cancella_commento"),
    path('articolo/aggiorna-articolo/<str:slug>/', views.AggiornaArticolo.as_view(), name="aggiorna_articolo"),   
    path('articolo/<str:slug>/elimina/', views.CancellaArticolo.as_view(), name="cancella_articolo"),
]