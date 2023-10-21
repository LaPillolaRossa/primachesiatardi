from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class ModelloContatto(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    email = models.EmailField()
    oggetto = models.CharField(max_length=100)
    contenuto = models.TextField(max_length=5000)
    file = models.FileField(upload_to="uploads_utenti/%Y/%m/%d/", blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpeg','jpg', 'png', 'docx', 'xlsx', 'MOV','avi','mp4','webm','mkv'])])
    
    
    def __str__(self):
        return self.oggetto
    
    class Meta:
        verbose_name = "Richieste Visitatori"
        verbose_name_plural = "Richieste Visitatori"
    