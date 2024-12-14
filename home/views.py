from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages
from django.http import Http404

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
    if id:  # Se o ID for fornecido, tenta buscar o registro
        categoria = get_object_or_404(Categoria, id=id)
    else:  # Se não, cria uma nova instância
        categoria = None

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()  # Salva no banco de dados
            messages.success(request, 'Categoria salva com sucesso!')
            return redirect('categoria')  # Redireciona para a listagem
    else:
        form = CategoriaForm(instance=categoria)  # Formulário com a instância existente ou vazio

    return render(request, 'categoria/formulario.html', {'form': form})

def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.success(request, 'Categoria excluída com sucesso!')
    return redirect('categoria')  # Redireciona para a listagem de categorias

def detalhes_categoria(request, id):
    try:
        categoria = get_object_or_404(Categoria, pk=id)
        categoria_encontrada = True
    except Http404:
        categoria = None
        categoria_encontrada = False
    return render(request, 'categoria/detalhes.html', {'categoria': categoria, 'categoria_encontrada': categoria_encontrada})
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('id')
    return render(request, 'cliente/lista_clientes.html', {'clientes': clientes})


def form_cliente(request, id=None):
    if id:  # Se o ID for fornecido, tenta buscar o registro
        cliente = get_object_or_404(Cliente, id=id)
    else:  # Se não, cria uma nova instância
        cliente = None

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()  # Salva no banco de dados
            messages.success(request, 'Cliente salvo com sucesso!')
            return redirect('lista_clientes')  # Redireciona para a listagem
    else:
        form = ClienteForm(instance=cliente)  # Formulário com a instância existente ou vazio

    return render(request, 'cliente/formulario.html', {'form': form})

def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, 'Cliente excluído com sucesso!')
    return redirect('lista_clientes')  # Redireciona para a listagem de clientes

def detalhes_cliente(request, id):
    try:
        cliente = get_object_or_404(Cliente, pk=id)
        cliente_encontrado = True
    except Http404:
        cliente = None
        cliente_encontrado = False
    return render(request, 'cliente/detalhes_cliente.html', {'cliente': cliente, 'cliente_encontrado': cliente_encontrado})
