from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404

from livros.models import Livro, UsuarioLivro
from accounts.views import superuser_required

# Create your views here.
@superuser_required()
class CriaLivro(LoginRequiredMixin,generic.CreateView):
    fields = ('titulo', 'num_paginas', 'data_publicacao', 'total_de_notas',
            'nota_media', 'autor', 'editora', 'genero')
    model = Livro

    redirect_field_name = 'livros/livro_detail.html'


class UmLivro(generic.DetailView):
    model = Livro

class ListaLivro(generic.ListView):
    model = Livro

class IncluiLivroNaLista(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args,**kwargs):
        return reverse('livros:single',kwargs={'pk':self.kwargs.get('pk')})

    def get(self,request,*args,**kwargs):
        livro = get_object_or_404(Livro, pk=self.kwargs.get('pk'))

        try:
            UsuarioLivro.objects.create(usuario_id=self.request.user, livro_id=livro)
        except IntegrityError:
            messages.warning(self.request,'Você já tem o livro na lista')
        else:
            messages.success(self.request,'O livro foi incluido na sua lista!')

        return super().get(request,*args,**kwargs)

class RetiraLivroDaLista(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args,**kwargs):
        return reverse('livros:single',kwargs={'pk':self.kwargs.get('pk')})

    def get(self,request,*args,**kwargs):

        try:
            leitor = UsuarioLivro.objects.filter(
                usuario_id=self.request.user,
                livro_id__pk=self.kwargs.get('pk')
            ).get()
        except UsuarioLivro.DoesNotExist:
            messages.warning(self.request,'Desculpa, esse livro não se encontra em sua lista!')
        else:
            leitor.delete()
            messages.success(self.request, 'O livro saiu da sua lista')

        return super().get(request,*args,**kwargs)

class ProcuraLivro(generic.ListView):
    model = Livro
    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        select_atribute =  self.request.GET.get('select_atribute')

        if query:
            if select_atribute == 'titulo':
                object_list = self.model.objects.filter(titulo__icontains=query)
            elif select_atribute == 'autor':
                object_list = self.model.objects.filter(autor__nome_autor__icontains=query)
            elif select_atribute == 'editora':
                object_list = self.model.objects.filter(editora__nome_editora__icontains=query)
            elif select_atribute == 'genero':
                object_list = self.model.objects.filter(genero__genero__icontains=query)
            else:
                object_list = self.model.objects.none()
        else:
            object_list = self.model.objects.none()
        return object_list
