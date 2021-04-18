from django.db import models

# Create your models here.
class Genero(models.Model):
    genero = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.genero

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
