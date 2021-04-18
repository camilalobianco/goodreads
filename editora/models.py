from django.db import models

# Create your models here.
class Editora(models.Model):
    nome_editora = models.CharField(max_length=50, unique=True)
    localizacao = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome_editora

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
