from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categorias/', views.lista_categorias, name='lista_categorias'),  # Lista de categorias
    path('categoria/formulario/', views.form_categoria, name='form_categoria'),  # Criação de categoria
    path('categoria/formulario/<int:id>/', views.form_categoria, name='form_categoria'),  # Edição de categoria
    path('categoria/excluir/<int:id>/', views.excluir_categoria, name='excluir_categoria'),  # Excluir categoria
    path('categoria/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),  # Detalhes da categoria
    path('produtos/', views.lista_produtos, name='lista_produtos'),  # Lista de produtos
    path('produto/formulario/', views.form_produto, name='form_produto'),  # Criação de produto
    path('produto/formulario/<int:id>/', views.form_produto, name='form_produto'),  # Edição de produto
    path('produto/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),  # Excluir produto
    path('produto/<int:id>/', views.detalhes_produto, name='detalhes_produto'),  # Detalhes do produto
    path('clientes/', views.lista_clientes, name='lista_clientes'),  # Lista de clientes
    path('cliente/formulario/', views.form_cliente, name='form_cliente'),  # Criação de cliente
    path('cliente/formulario/<int:id>/', views.form_cliente, name='form_cliente'),  # Edição de cliente
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),  # Excluir cliente
    path('cliente/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),  # Detalhes do cliente
]
