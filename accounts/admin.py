from django.contrib import admin
from django.contrib.auth.models import User
from . import models
# Register your models here.
class ProfileInline(admin.TabularInline):
    model = models.Profile


admin.site.register(models.Profile)
