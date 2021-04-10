from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from livros.models import Livro
# Create your models here.
User = get_user_model()

class Resenha(models.Model):
    livro = models.ForeignKey(Livro, related_name='resenhas',on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(max_length=150)
    data_publicacao = models.DateTimeField(default=timezone.now)
    resenha_aprovada = models.BooleanField(default=False)

    def approve(self):
        self.resenha_aprovada = True
        self.save()

    def get_absolute_url(self):
        return reverse("livros:single", kwargs={'pk':self.pk})

    def __str__(self):
        return self.resenha
