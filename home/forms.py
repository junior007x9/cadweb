from django import forms
from .models import *
from .models import Cliente
from django import forms
from .models import Produto
from .models import Estoque
from .models import Categoria
from .models import Pedido
from datetime import date
from .models import Pagamento
from .models import ItemPedido
from django.core.exceptions import ValidationError

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'),
        }

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc >= date.today():
            raise ValidationError('A data de nascimento não pode ser maior ou igual à data atual.')
        return datanasc


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'qtde']
        widgets = {
            'produto': forms.HiddenInput(),  # Campo oculto para armazenar o ID do produto
            'qtde': forms.TextInput(attrs={'class': 'inteiro form-control'}),
        }


class ProdutoForm(forms.ModelForm):
    qtde = forms.IntegerField(label='Quantidade em Estoque', initial=0, min_value=0)

    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64', 'qtde']
        widgets = {
            'categoria': forms.HiddenInput(),  # Campo oculto para armazenar o ID da categoria
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'img_base64': forms.HiddenInput(),
            'preco': forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }
        labels = {
            'nome': 'Nome do Produto',
            'preco': 'Preço do Produto',
        }

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True

    def save(self, commit=True):
        produto = super().save(commit=False)
        if commit:
            produto.save()
            Estoque.objects.update_or_create(produto=produto, defaults={'qtde': self.cleaned_data['qtde']})
        return produto




class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput(),  # Campo oculto para armazenar o ID
        }
class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido', 'produto', 'qtde']
        widgets = {
            'pedido': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'produto': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            'qtde': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_qtde(self):
        qtde = self.cleaned_data.get('qtde')
        if not isinstance(qtde, int) or qtde < 0:
            raise ValidationError('A quantidade deve ser um número inteiro positivo.')
        return qtde
    
#class pagamento


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pedido', 'forma', 'valor']
        widgets = {
            'pedido': forms.HiddenInput(),  # Campo oculto para armazenar o ID
            # Usando Select para renderizar as opções
            'forma': forms.Select(attrs={'class': 'form-control'}),  
            'valor': forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PagamentoForm, self).__init__(*args, **kwargs)
        self.fields['valor'].localize = True
        self.fields['valor'].widget.is_localized = True       
