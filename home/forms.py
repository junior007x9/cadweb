from django import forms
from .models import *
from .models import Cliente
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'),
        }
