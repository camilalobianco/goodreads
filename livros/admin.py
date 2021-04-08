from django.contrib import admin
from . import models
# Register your models here.
class UsuarioLivroInline(admin.TabularInline):
    model = models.UsuarioLivro

admin.site.register(models.Livro)
