from django.db import models
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

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

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'
