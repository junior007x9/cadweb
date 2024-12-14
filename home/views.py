from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Cliente, Produto
from .forms import CategoriaForm, ClienteForm, ProdutoForm
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

# Views para Categoria
def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('-criado_em')  # Ordena por data de criação em ordem decrescente
    return render(request, 'categoria/lista.html', {'categorias': categorias})


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
            return redirect('lista_categorias')  # Redireciona para a listagem
    else:
        form = CategoriaForm(instance=categoria)  # Formulário com a instância existente ou vazio

    return render(request, 'categoria/formulario.html', {'form': form})

def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
    return redirect('lista_categorias')  # Redireciona para a listagem de categorias

def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
        return render(request, 'categoria/detalhes.html', {'categoria': categoria})
    except Categoria.DoesNotExist:
        messages.error(request, 'Categoria não encontrada.')
        return redirect('lista_categorias')  # Redireciona para a lista de categorias

# Views para Cliente
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-criado_em')  # Ordena por data de criação em ordem decrescente
    return render(request, 'cliente/lista.html', {'clientes': clientes})


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
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('lista_clientes')  # Redireciona para a listagem de clientes
    return render(request, 'cliente/confirmar_exclusao.html', {'cliente': cliente})

def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        return render(request, 'cliente/detalhes.html', {'cliente': cliente})
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('lista_clientes')  # Redireciona para a lista de clientes

# Views para Produto
def lista_produtos(request):
    produtos = Produto.objects.all().order_by('-criado_em')  # Ordena por data de criação em ordem decrescente
    return render(request, 'produto/lista.html', {'produtos': produtos})



def form_produto(request, id=None):
    if id:  # Se o ID for fornecido, tenta buscar o registro
        produto = get_object_or_404(Produto, id=id)
    else:  # Se não, cria uma nova instância
        produto = None

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()  # Salva no banco de dados
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('lista_produtos')  # Redireciona para a listagem
    else:
        form = ProdutoForm(instance=produto)  # Formulário com a instância existente ou vazio

    return render(request, 'produto/formulario.html', {'form': form})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('lista_produtos')  # Redireciona para a listagem de produtos
    return render(request, 'produto/confirmar_exclusao.html', {'produto': produto})

def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(id=id)
        return render(request, 'produto/detalhes.html', {'produto': produto})
    except Produto.DoesNotExist:
        messages.error(request, 'Produto não encontrado.')
        return redirect('lista_produtos')  # Redireciona para a lista de produtos
