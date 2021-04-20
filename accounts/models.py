from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400)
    foto_de_perfil = models.ImageField(upload_to='accounts/fotos_de_perfil/',blank=True, default='', null=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('accounts:profile',kwargs={'pk':self.pk})
