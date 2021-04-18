from django.contrib import admin
from . import models
# Register your models here.
class GeneroInline(admin.TabularInline):
    model = models.Genero

admin.site.register(models.Genero)
