from django.db import models
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError

# Modelo para Categoria
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

# Modelo para Produto
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(default=timezone.now)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)  # Campo para armazenar a imagem em base64

    def __str__(self):
        return self.nome

    @property
    def estoque(self):
        estoque_item, created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item

# Modelo para Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

    @property
    def datanascimento(self):
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None

    def clean(self):
        if self.datanasc and self.datanasc >= date.today():
            raise ValidationError('A data de nascimento não pode ser maior ou igual à data atual.')

# Modelo para Estoque
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'

# Modelo para ItemPedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        """Calcula o total do item do pedido"""
        return self.qtde * self.preco

    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"


# Modelo para Pedido
class Pedido(models.Model):
    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4

    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through=ItemPedido)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

    @property
    def data_pedidof(self):
        return self.data_pedido.strftime('%d/%m/%Y %H:%M')

    @property
    def total(self):
        """Calcula o total de todos os itens no pedido, formatado como moeda local"""
        total = sum(item.qtde * item.preco for item in self.itempedido_set.all())
        return total

    @property
    def qtdeItens(self):
        """Conta a quantidade de itens no pedido"""
        return self.itempedido_set.count()
