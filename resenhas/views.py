from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Resenha
from livros.models import Livro
from .forms import ResenhaForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@login_required
def adiciona_resenha(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == "POST":
        form = ResenhaForm(request.POST)
        if form.is_valid():
            resenha = form.save(commit=False)
            resenha.livro = livro
            resenha.usuario = request.user
            resenha.save()
            return redirect('livros:single', pk=livro.pk)
    else:
        form = ResenhaForm()
    return render(request, 'resenhas/resenha_form.html', {'form': form})



@user_passes_test(lambda u: u.is_superuser)
def aprova_resenha(request, pk):
    resenha = get_object_or_404(Resenha, pk=pk)
    resenha.approve()
    return redirect('livros:single', pk=resenha.livro.pk)

@user_passes_test(lambda u: u.is_superuser)
def remove_resenha(request, pk):
    resenha = get_object_or_404(Resenha, pk=pk)
    livro_pk = resenha.livro.pk
    resenha.delete()
    return redirect('livros:single', pk=livro_pk)
