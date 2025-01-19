from django.urls import path
from . import views

urlpatterns = [
    # Index
    path('', views.index, name="index"),

    # Categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categoria/formulario/', views.form_categoria, name='form_categoria'),
    path('categoria/formulario/<int:id>/', views.form_categoria, name='form_categoria'),
    path('categoria/excluir/<int:id>/', views.excluir_categoria, name='excluir_categoria'),
    path('categoria/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),

    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente/formulario/', views.form_cliente, name='form_cliente'),
    path('cliente/formulario/<int:id>/', views.form_cliente, name='form_cliente'),
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('cliente/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),

    # Produtos
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produto/formulario/', views.form_produto, name='form_produto'),
    path('produto/formulario/<int:id>/', views.form_produto, name='form_produto'),
    path('produto/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('produto/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    path('editar_produto/<int:id>/', views.editar_produto, name='editar_produto'),
    path('ajustar_estoque/<int:id>/', views.ajustar_estoque, name='ajustar_estoque'),

    # Testes
    path('teste1/', views.teste1, name='teste1'),
    path('teste2/', views.teste2, name='teste2'),
    path('teste3/', views.teste3, name='teste3'),

    # Buscar Dados
    path('buscar_dados/<str:app_modelo>/', views.buscar_dados, name='buscar_dados'),
]