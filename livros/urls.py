from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'livros'
urlpatterns = [
    url(r'^$', views.ListaLivro.as_view(), name='all'),
    url(r'^new/$', views.CriaLivro.as_view(), name='create'),
    url(r'in/(?P<pk>[-\w]+)/$', views.UmLivro.as_view(), name='single'),
    path(r'join/(?P<pk>[-\w]+)/$', views.IncluiLivroNaLista.as_view(), name='join'),
    path(r'leave/(?P<pk>[-\w]+)/$', views.RetiraLivroDaLista.as_view(), name='leave'),
]
