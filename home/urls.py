from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categorias/', views.categoria, name='categoria'),  # Lista de categorias
    path('produtos/', views.lista_produtos, name='lista_produtos'),  # Lista de produtos
    path('formulario/', views.form_categoria, name='form_categoria'),  # Criação
    path('formulario/<int:id>/', views.form_categoria, name='form_categoria'),  # Edição
    path('produtos/excluir/<int:id>/', views.excluir_categoria, name='excluir_categoria'),  # Excluir
    path('categoria/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),  # Detalhes
    path('clientes/', views.lista_clientes, name='lista_clientes'),  # Lista de clientes
    path('cliente/formulario/', views.form_cliente, name='form_cliente'),  # Criação de cliente
    path('cliente/formulario/<int:id>/', views.form_cliente, name='form_cliente'),  # Edição de cliente
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),  # Excluir cliente
    path('cliente/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),  # Detalhes do cliente
]
