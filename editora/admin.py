from django.contrib import admin
from . import models
# Register your models here.
class EditoraInline(admin.TabularInline):
    model = models.Editora

admin.site.register(models.Editora)
