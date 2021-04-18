from django.contrib import admin
from . import models
# Register your models here.
class AutorInLine(admin.TabularInline):
    model = models.Autor

admin.site.register(models.Autor)
# Register your models here.
