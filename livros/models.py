from django.db import models
from django.contrib.auth import get_user_model
from django import template
from django.db import models
from django.urls import reverse
from autor.models import Autor
from genero.models import Genero
from editora.models import Editora

# Create your models here.
User = get_user_model()
register = template.Library()

class Livro(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE,  default='')
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE,  default='')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE,  default='')
    titulo = models.CharField(max_length=50, unique=True)
    nota_media = models.DecimalField(blank=True, max_digits=3, decimal_places=1)
    num_paginas = models.IntegerField()
    data_publicacao = models.DateField()
    total_de_notas = models.IntegerField()
    capa = models.ImageField(upload_to='livros/capas/',blank=True, default='', null=True)
    leitores = models.ManyToManyField(User,through="UsuarioLivro")

    def __str__(self):
        return self.titulo

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('livros:single',kwargs={'pk':self.pk})

    class Meta:
        ordering = ['titulo']


class UsuarioLivro(models.Model):
    livro_id   = models.ForeignKey(Livro,related_name='leitor', on_delete=models.CASCADE)
    usuario_id = models.ForeignKey(User, related_name='livro_usuario', on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario_id.username

    class Meta:
        unique_together = ('livro_id','usuario_id')
