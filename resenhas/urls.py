from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'resenhas'

urlpatterns = [
    path('<int:pk>/', views.adiciona_resenha, name='adiciona_resenha'),
    path('<int:pk>/aprova/', views.aprova_resenha, name='aprova_resenha'),
    path('<int:pk>/remove/', views.remove_resenha, name='remove_resenha'),
]
