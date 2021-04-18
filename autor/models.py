from django.db import models

# Create your models here.
class Autor(models.Model):
    nome_autor =  models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nome_autor

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
