from django.conf.urls import url
from django.urls import re_path, include, path
from . import views

app_name = 'livros'
urlpatterns = [
    re_path(r'search/$', views.ProcuraLivro.as_view(), name='search'),
    url(r'^all/', views.ListaLivro.as_view(), name='all'),
    url(r'^new/$', views.CriaLivro.as_view(), name='create'),
    url(r'in/(?P<pk>[-\w]+)/$', views.UmLivro.as_view(), name='single'),
    path('join/<int:pk>', views.IncluiLivroNaLista.as_view(), name='join'),
    path('leave/<int:pk>/', views.RetiraLivroDaLista.as_view(), name='leave'),
    #re_path('<int:pk>/resenhas',include("resenhas.urls", namespace="resenhas")),
]
