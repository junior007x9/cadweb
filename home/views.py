from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm, PedidoForm, ItemPedidoForm
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps

# Views para Página Inicial
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
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('lista_produtos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
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
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=produto.estoque)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = EstoqueForm(instance=produto.estoque)
    return render(request, 'produto/estoque.html', {'form': form})

# Views de Teste
def teste1(request):
    return render(request, 'testes/teste1.html')

def teste2(request):
    return render(request, 'testes/teste2.html')

def teste3(request):
    return render(request, "testes/teste3.html")

# Função para buscar dados
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

# Views para Pedido
def pedido(request):
    lista = Pedido.objects.all().order_by('id')
    return render(request, 'pedido/lista.html', {'lista': lista})

def novo_pedido(request, id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            # Caso o registro não seja encontrado, exibe a mensagem de erro
            messages.error(request, 'Registro não encontrado')
            return redirect('lista_clientes')  # Redireciona para a listagem de clientes
        # cria um novo pedido com o cliente selecionado
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)  # cria um formulário com o novo pedido
        return render(request, 'pedido/form.html', {'form': form})
    else:  # se for método POST, salva o pedido.
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('pedido')
        else:
            messages.error(request, 'Erro ao salvar o pedido. Por favor, corrija os erros abaixo.')
            return render(request, 'pedido/form.html', {'form': form})

def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else:  # method POST
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.preco = item_pedido.produto.preco

            # Realizar aqui o tratamento do estoque
            estoque_atual = item_pedido.produto.estoque
            if item_pedido.qtde > estoque_atual.qtde:
                messages.error(request, 'Estoque insuficiente para o produto solicitado')
            else:
                estoque_atual.qtde -= item_pedido.qtde
                estoque_atual.save()
                item_pedido.save()
                messages.success(request, 'Item adicionado ao pedido com sucesso!')
                return redirect('detalhes_pedido', id=pedido.id)
        else:
            messages.error(request, 'Erro ao adicionar produto. Por favor, corrija os erros abaixo.')

    itens_pedido = pedido.itempedido_set.all()
    contexto = {
        'pedido': pedido,
        'form': form,
        'itens_pedido': itens_pedido,
    }
    return render(request, 'pedido/detalhes.html', contexto)

def editar_pedido(request, id):
    # Implemente a lógica de edição de pedido aqui
    # Por exemplo, você pode querer reutilizar a lógica de novo_pedido ou detalhes_pedido com algumas modificações
    pedido = get_object_or_404(Pedido, id=id)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido atualizado com sucesso!')
            return redirect('detalhes_pedido', id=pedido.id)
        else:
            messages.error(request, 'Erro ao atualizar o pedido. Por favor, corrija os erros abaixo.')
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'pedido/form.html', {'form': form})

def excluir_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido excluído com sucesso.')
        return redirect('pedido')

    contexto = {
        'pedido': pedido,
    }
    return render(request, 'pedido/confirmar_exclusao.html', contexto)

# Views para ItemPedido
def editar_item_pedido(request, id):
    item_pedido = get_object_or_404(ItemPedido, id=id)
    
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.preco = item_pedido.produto.preco

            # Realizar aqui o tratamento do estoque
            estoque_atual = item_pedido.produto.estoque
            if item_pedido.qtde > estoque_atual.qtde:
                messages.error(request, 'Estoque insuficiente para o produto solicitado')
            else:
                estoque_atual.qtde -= item_pedido.qtde
                estoque_atual.save()
                item_pedido.save()
                messages.success(request, 'Item atualizado com sucesso!')
                return redirect('detalhes_pedido', id=item_pedido.pedido.id)
        else:
            messages.error(request, 'Erro ao atualizar o item do pedido. Por favor, corrija os erros abaixo.')
    else:
        form = ItemPedidoForm(instance=item_pedido)

    contexto = {
        'form': form,
        'pedido': item_pedido.pedido,
        'item_pedido': item_pedido,
    }
    return render(request, 'pedido/editar_item.html', contexto)

def excluir_item_pedido(request, id):
    item_pedido = get_object_or_404(ItemPedido, id=id)
    pedido_id = item_pedido.pedido.id
    
    if request.method == 'POST':
        item_pedido.delete()
        messages.success(request, 'Item do pedido excluído com sucesso.')
        return redirect('detalhes_pedido', id=pedido_id)

    contexto = {
        'item_pedido': item_pedido,
        'pedido': item_pedido.pedido,
    }
    return render(request, 'pedido/confirmar_exclusao_item.html', contexto)
