from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Resenha(models.Model):
    livro = models.ForeignKey('livros.Livro', related_name='comments',on_delete=models.CASCADE)
    usuario = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    resenha = models.TextField(max_length=150)
    created_date = models.DateTimeField(default=timezone.now)
    resenha_aprovada = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_single")

    def __str__(self):
        return self.text
