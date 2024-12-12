from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import Http404, HttpResponseNotFound



def index(request):
    return render(request, 'index.html')

def categoria(request):
    # Exibe a lista de categorias
    contexto = {
        'lista': Categoria.objects.all().order_by('id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def lista_produtos(request):
    # Exibe a lista de produtos
    lista = Categoria.objects.all()  
    return render(request, 'categoria/lista.html', {'lista': lista})



def form_categoria(request, id=None):
    if id:
        categoria = get_object_or_404(Categoria, pk=id)
        if request.method == 'POST':
            form = CategoriaForm(request.POST, instance=categoria)  # formulário com os dados existentes
            if form.is_valid():
                categoria = form.save()  # salva a instancia do modelo no banco de dados
                messages.success(request, 'Operação realizada com Sucesso')
                return redirect('categoria')  # redireciona para a listagem
        else:  # método é GET, editando registro existente
            form = CategoriaForm(instance=categoria)  # formulário preenchido com os dados existentes
    else:
        if request.method == 'POST':
            form = CategoriaForm(request.POST)  # instancia o modelo com os dados do form
            if form.is_valid():  # faz a validação do formulário
                categoria = form.save()  # salva a instancia do modelo no banco de dados
                messages.success(request, 'Operação realizada com Sucesso')
                return redirect('categoria')  # redireciona para a listagem
        else:  # método é GET, novo registro
            form = CategoriaForm()  # formulário vazio
    contexto = {
        'form': form,
    }
    return render(request, 'categoria/formulario.html', contexto)


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)  # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        if form.is_valid():
            categoria = form.save()  # save retorna o objeto salvo
            messages.success(request, 'Operação realizada com Sucesso')
            lista = [categoria] 
            return render(request, 'categoria/lista.html', {'lista': lista})
    else:
        form = CategoriaForm(instance=categoria)  # formulário preenchido com os dados existentes
    return render(request, 'categoria/formulario.html', {'form': form})


def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    categoria.delete()
    messages.success(request, 'Operação realizada com Sucesso')
    return redirect('categoria')  # redireciona para a listagem de categorias

def detalhes_categoria(request, id):
    try:
        categoria = get_object_or_404(Categoria, pk=id)
        categoria_encontrada = True
    except Http404:
        categoria = None
        categoria_encontrada = False
    return render(request, 'categoria/detalhes.html', {'categoria': categoria, 'categoria_encontrada': categoria_encontrada})
