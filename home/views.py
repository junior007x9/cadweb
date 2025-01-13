from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Cliente, Produto, Estoque
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm
from django.contrib import messages



def index(request):
    return render(request, 'index.html')

# Views para Categoria
def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('-criado_em')
    return render(request, 'categoria/lista.html', {'categorias': categorias})

def form_categoria(request, id=None):
    if id:
        categoria = get_object_or_404(Categoria, id=id)
    else:
        categoria = None

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            if not messages.get_messages(request):
                messages.success(request, 'Operação realizada com sucesso!')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categoria/formulario.html', {'form': form})

def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        if not messages.get_messages(request):
            messages.success(request, 'Operação realizada com sucesso!')
        return redirect('lista_categorias')

def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
        return render(request, 'categoria/detalhes.html', {'categoria': categoria})
    except Categoria.DoesNotExist:
        return redirect('lista_categorias')

# Views para Cliente
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-criado_em')
    return render(request, 'cliente/lista.html', {'clientes': clientes})

def form_cliente(request, id=None):
    if id:
        cliente = get_object_or_404(Cliente, id=id)
    else:
        cliente = None

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('lista_clientes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'cliente/formulario.html', {'form': form})



def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        if not messages.get_messages(request):
            messages.success(request, 'Operação realizada com sucesso!')
        return redirect('lista_clientes')

def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        return render(request, 'cliente/detalhes.html', {'cliente': cliente})
    except Cliente.DoesNotExist:
        return redirect('lista_clientes')

# Views para Produto
def lista_produtos(request):
    produtos = Produto.objects.all().order_by('-criado_em')
    return render(request, 'produto/lista.html', {'produtos': produtos})


def form_produto(request, id=None):
    if id:
        produto = get_object_or_404(Produto, id=id)
    else:
        produto = None

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            produto = form.save(commit=False)
            img_base64 = request.POST.get('img_base64')
            if img_base64:
                produto.img_base64 = img_base64
            produto.save()
            if not messages.get_messages(request):
                messages.success(request, 'Operação realizada com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produto/form.html', {'form': form})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        if not messages.get_messages(request):
            messages.success(request, 'Operação realizada com sucesso!')
        return redirect('lista_produtos')

def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(id=id)
        return render(request, 'produto/detalhes.html', {'produto': produto})
    except Produto.DoesNotExist:
        return redirect('lista_produtos')


def editar_produto(request, id):
    return form_produto(request, id)

def ajustar_estoque(request, id):
    produto = Produto.objects.get(pk=id)
    estoque = produto.estoque  # Pega o objeto estoque relacionado ao produto
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            lista = []
            lista.append(estoque.produto)
            return render(request, 'produto/lista.html', {'produtos': lista})
    else:
        form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form})