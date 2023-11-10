from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from hitcount.models import HitCount
import math

# Create your models here.

class Sezione(models.Model):
    """
    le sezioni dividono il sito per categorie di articoli.
    Ciascuna sezione contiene svariati articoli,
    creati dagli utenti del sito.
    """
    nome_sezione = models.CharField(max_length=80)
    descrizione = models.CharField(max_length=150, blank=True, null=True)
    logo_sezione = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.nome_sezione
    
    def get_absolute_url(self):
        return reverse("sezione_view", kwargs={"pk": self.pk})
    
    def get_last_articles(self):
        return Articolo.objects.filter(sezione_appartenenza=self).order_by("-data_creazione")[:10]
    
    def get_number_of_comments_in_section(self):
        return Commento.objects.filter(articolo__sezione_appartenenza=self).count()
    
    class Meta:
        verbose_name = "Sezione"
        verbose_name_plural = "Sezioni"
        
        
class Articolo(models.Model):
    titolo = models.CharField(max_length=255)
    contenuto = RichTextUploadingField(blank=True, null=True)
    immagine = models.ImageField(blank=True, null=True)
    data_creazione = models.DateTimeField(auto_now_add=True)
    autore_articolo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articoli")
    sezione_appartenenza = models.ForeignKey(Sezione, on_delete=models.CASCADE, blank=True, null=True)
    like_articolo = models.ManyToManyField(User, related_name="likes_articoli")
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    slug = models.SlugField(max_length=255, null=True)
    
    def __str__(self):
        return self.titolo
    
    def get_absolute_url(self):
        return reverse("visualizza_articolo", kwargs={"slug": self.slug})
    
    def get_n_pages(self):
        commenti = self.commento_set.count()
        n_pagine = math.ceil(commenti / 10)
        return n_pagine
    
    def get_total_like_articolo(self):
        return self.like_articolo.count()
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.titolo)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Articolo"
        verbose_name_plural = "Articoli"
        
        
class Commento(models.Model):
    autore_commento = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenti")    
    contenuto = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)
    articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.autore_commento.username    

    
    class Meta:
        verbose_name = "Commento"
        verbose_name_plural = "Commenti"
