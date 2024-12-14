from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria
from .forms import CategoriaForm
from django.contrib import messages
from django.http import Http404, HttpResponseNotFound


def index(request):
    return render(request, 'index.html')


def categoria(request):
    try:
        contexto = {
            'lista': Categoria.objects.all().order_by('-created_at'),
        }
        return render(request, 'categoria/lista.html', contexto)
    except Http404:
        return HttpResponseNotFound('Categorias não encontradas')


def lista_produtos(request):
    try:
        lista = Categoria.objects.all().order_by('-created_at')
        return render(request, 'categoria/lista.html', {'lista': lista})
    except Http404:
        return HttpResponseNotFound('Produtos não encontrados')


def form_categoria(request, id=None):
    if id:
        categoria = get_object_or_404(Categoria, pk=id)
        if request.method == 'POST':
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                categoria = form.save()
                messages.success(request, 'Operação realizada com Sucesso')
                return redirect('categoria')
        else:
            form = CategoriaForm(instance=categoria)
    else:
        if request.method == 'POST':
            form = CategoriaForm(request.POST)
            if form.is_valid():
                categoria = form.save()
                messages.success(request, 'Operação realizada com Sucesso')
                return redirect('categoria')
        else:
            form = CategoriaForm()
    contexto = {'form': form}
    return render(request, 'categoria/formulario.html', contexto)


def editar_categoria(request, id):
    try:
        categoria = get_object_or_404(Categoria, pk=id)
        if request.method == 'POST':
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                categoria = form.save()
                messages.success(request, 'Operação realizada com Sucesso')
                lista = [categoria]
                return render(request, 'categoria/lista.html', {'lista': lista})
        else:
            form = CategoriaForm(instance=categoria)
        return render(request, 'categoria/formulario.html', {'form': form})
    except Http404:
        return HttpResponseNotFound('Categoria não encontrada')


def excluir_categoria(request, id):
    try:
        categoria = get_object_or_404(Categoria, pk=id)
        categoria.delete()
        messages.success(request, 'Operação realizada com Sucesso')
        return redirect('categoria')
    except Http404:
        return HttpResponseNotFound('Categoria não encontrada')


def detalhes_categoria(request, id):
    try:
        categoria = get_object_or_404(Categoria, pk=id)
        categoria_encontrada = True
    except Http404:
        categoria = None
        categoria_encontrada = False
    return render(request, 'categoria/detalhes.html', {'categoria': categoria, 'categoria_encontrada': categoria_encontrada})
