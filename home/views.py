from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido, Pagamento
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm, PedidoForm, ItemPedidoForm, PagamentoForm
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .models import Pedido
from django.contrib import messages
# Views para Página Inicial
@login_required
def index(request):
    return render(request, 'index.html')

# Views para Categoria
@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('-criado_em')
    return render(request, 'categoria/lista.html', {'categorias': categorias})
@login_required
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
@login_required
def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        if not messages.get_messages(request):
            messages.success(request, 'Operação realizada com sucesso!')
        return redirect('lista_categorias')
@login_required
def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
        return render(request, 'categoria/detalhes.html', {'categoria': categoria})
    except Categoria.DoesNotExist:
        return redirect('lista_categorias')

# Views para Cliente
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-criado_em')
    return render(request, 'cliente/lista.html', {'clientes': clientes})
@login_required
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
@login_required
def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        if not messages.get_messages(request):
            messages.success(request, 'Operação realizada com sucesso!')
        return redirect('lista_clientes')
@login_required
def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        return render(request, 'cliente/detalhes.html', {'cliente': cliente})
    except Cliente.DoesNotExist:
        return redirect('lista_clientes')

# Views para Produto
@login_required
def lista_produtos(request):
    produtos = Produto.objects.all().order_by('-criado_em')
    return render(request, 'produto/lista.html', {'produtos': produtos})
@login_required
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
@login_required
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        if not messages.get_messages(request):
            messages.success(request, 'Operação realizada com sucesso!')
        return redirect('lista_produtos')
@login_required
def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(id=id)
        return render(request, 'produto/detalhes.html', {'produto': produto})
    except Produto.DoesNotExist:
        return redirect('lista_produtos')
@login_required
def editar_produto(request, id):
    return form_produto(request, id)
@login_required
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
@login_required
def teste1(request):
    return render(request, 'testes/teste1.html')
@login_required
def teste2(request):
    return render(request, 'testes/teste2.html')
@login_required
def teste3(request):
    return render(request, "testes/teste3.html")

# Função para buscar dados
@login_required
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
@login_required
def pedido(request):
    lista = Pedido.objects.all().order_by('id')
    return render(request, 'pedido/lista.html', {'lista': lista})
@login_required
def novo_pedido(request, id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Registro não encontrado')
            return redirect('lista_clientes')
        
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido/form.html', {'form': form})
    
    else:
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedido')
        else:
            messages.error(request, 'Erro ao salvar o pedido. Por favor, corrija os erros abaixo.')
            return render(request, 'pedido/form.html', {'form': form})
@login_required
def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else:
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            item_pedido.preco = item_pedido.produto.preco

            # Tratamento do estoque
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
@login_required
def editar_pedido(request, id):
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


# Views para ItemPedido
@login_required
def editar_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)
         
    pedido = item_pedido.pedido
    quantidade_anterior = item_pedido.qtde

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)

            # Tratamento do estoque
            nova_quantidade = item_pedido.qtde
            estoque_atual = item_pedido.produto.estoque.qtde  # Acessando a quantidade do estoque diretamente
            
            if nova_quantidade > (estoque_atual + quantidade_anterior):
                messages.error(request, 'Quantidade em estoque insuficiente para o produto.')
            else:
                # Ajusta o estoque considerando a quantidade anterior
                estoque_atual += quantidade_anterior  # Devolve a quantidade anterior ao estoque
                estoque_atual -= nova_quantidade  # Subtrai a nova quantidade do estoque
                item_pedido.produto.estoque.qtde = estoque_atual  # Atualiza a quantidade de estoque
                item_pedido.produto.estoque.save()
                item_pedido.save()
                messages.success(request, 'Operação realizada com sucesso')
                return redirect('detalhes_pedido', id=pedido.id)
        else:
            messages.error(request, 'Erro ao atualizar o item do pedido. Por favor, corrija os erros abaixo.')
    else:
        form = ItemPedidoForm(instance=item_pedido)
        
    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido,
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
        pedido_id = item_pedido.pedido.id  # Armazena o ID do pedido antes de remover o item
        estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
        estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
        estoque.save()  # Salva as alterações no estoque
        item_pedido.delete()  # Remove o item do pedido
        messages.success(request, 'Operação realizada com Sucesso')
        return redirect('detalhes_pedido', id=pedido_id)
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')
#pagamento
@login_required
def form_pagamento(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.pedido = pedido
            pagamento.save()
            messages.success(request, 'Operação realizada com sucesso')
            return redirect('detalhes_pedido', id=pedido.id)
        else:
            messages.error(request, 'Erro ao registrar o pagamento. Por favor, corrija os erros abaixo.')
    else:
        pagamento = Pagamento(pedido=pedido)
        form = PagamentoForm(instance=pagamento)

    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/pagamento.html', contexto)
@login_required
def editar_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, id=id)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso.')
            return redirect('detalhes_pedido', id=pagamento.pedido.id)
        else:
            messages.error(request, 'Erro ao atualizar o pagamento. Por favor, corrija os erros abaixo.')
    else:
        form = PagamentoForm(instance=pagamento)

    contexto = {
        'form': form,
        'pedido': pagamento.pedido,
    }
    return render(request, 'pedido/pagamento.html', contexto)
@login_required
def excluir_pagamento(request, id):
    pagamento = get_object_or_404(Pagamento, id=id)
    pedido_id = pagamento.pedido.id
    pagamento.delete()
    messages.success(request, 'Pagamento excluído com sucesso.')
    return redirect('detalhes_pedido', id=pedido_id)
#loguin
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirecione para a home se o usuário já estiver logado

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Substitua 'home' pela URL desejada
    else:
        form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})

@login_required
def baixar_nota_fiscal_pdf(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

    itens_pedido = pedido.itempedido_set.all()
    context = {
        'pedido': pedido,
        'itens_pedido': itens_pedido
    }
    return render(request, 'pedido/nota_fiscal.html', context)
