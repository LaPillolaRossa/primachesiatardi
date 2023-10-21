from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.homepageview, name="homepage"),
    path('manifesto/', views.manifesto_view, name="manifesto"),
    path('user/<str:username>/', views.user_profile_view, name="user_profile"),
    path('cerca/', views.cerca, name="funzione_cerca"),
]