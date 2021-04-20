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

from django.db import connection

# Create your views here.
class CriaLivro(LoginRequiredMixin,generic.CreateView):
    print(connection.queries)
    fields = ('titulo', 'num_paginas', 'data_publicacao', 'total_de_notas',
            'nota_media', 'autor', 'editora', 'genero', 'capa')
    model = Livro

    redirect_field_name = 'livros/livro_detail.html'

class UmLivro(generic.DetailView):
    model = Livro
    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
            print(queryset.query)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

class ListaLivro(generic.ListView):
    model = Livro
    def get_queryset(self):
        object_list = self.model.objects.all()
        print(object_list.query)

        return object_list

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
        select_atribute =  self.request.GET.get('select_atribute')
        if query:
            if select_atribute == 'titulo':
                object_list = self.model.objects.filter(titulo__icontains=query)
                print(object_list.query)
            elif select_atribute == 'autor':
                object_list = self.model.objects.filter(autor__nome_autor__icontains=query)
                print(object_list.query)
            elif select_atribute == 'editora':
                object_list = self.model.objects.filter(editora__nome_editora__icontains=query)
                print(object_list.query)
            elif select_atribute == 'genero':
                object_list = self.model.objects.filter(genero__genero__icontains=query)
                print(object_list.query)
            else:
                object_list = self.model.objects.none()
        else:
            object_list = self.model.objects.none()
        return object_list
