from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from . import forms
from accounts.models import Profile
from livros.models import Livro
from django.db.models import Avg, Count
import itertools
import operator
# Create your views here.
#class SignUp(CreateView):
#    form_class = forms.UserCreateForm
#    success_url = reverse_lazy("login")
#    template_name = "accounts/signup.html"


def register(request):
    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = forms.UserCreateForm(data=request.POST)
        profile_form = forms.ProfileForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            #user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'foto_de_perfil' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.foto_de_perfil = request.FILES['foto_de_perfil']

            # Now save model
            profile.save()

            return redirect(reverse("accounts:login"))
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = forms.UserCreateForm()
        profile_form = forms.ProfileForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'accounts/signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,})



def most_common(querySet, atributo):
  L = []
  if atributo == "editora":
      for i in range(len(querySet)):
          L.append(querySet[i].editora.nome_editora)
  if atributo == "autor":
      for i in range(len(querySet)):
          L.append(querySet[i].autor.nome_autor)
  if atributo == "genero":
    for i in range(len(querySet)):
      L.append(querySet[i].genero.genero)
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'accounts/user_profile.html'

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        livros_lidos = Livro.objects.filter(leitores=self.request.user)
        paginas_lidas = 0
        context['livros_lidos'] = livros_lidos.count()
        if livros_lidos:
            for i in range(len(livros_lidos)):
                paginas_lidas += livros_lidos[i].num_paginas

            context['paginas_lidas'] = paginas_lidas
            context['editora_mais_lida'] = most_common(livros_lidos, "editora")
            context['autor_mais_lido'] = most_common(livros_lidos, "autor")
            context['genero_mais_lido'] = most_common(livros_lidos, "genero")
        else:
            context['paginas_lidas'] = 0


        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)

            if context_object_name:
                context[context_object_name] = self.object
        print(context)
        context.update(kwargs)
        return super().get_context_data(**context)

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

def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper
