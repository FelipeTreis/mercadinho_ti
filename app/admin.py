from django.contrib import admin

from .models import (CarrinhoProduto, Categoria, Estoque, MovimentoEstoque,
                     Produto, Venda)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'adicionado', 'atualizado',)
    search_fields = ('nome',)
    list_filter = ('nome', 'adicionado', 'atualizado',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'categoria', 'adicionado', 'atualizado',)
    search_fields = ('nome', 'descricao',)
    list_filter = ('categoria', 'adicionado', 'atualizado',)

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'quantidade', 'adicionado', 'atualizado',)
    search_fields = ('produto__nome',)
    list_filter = ('adicionado', 'atualizado',)
    readonly_fields = ('operacao', 'origem',)

@admin.register(MovimentoEstoque)
class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('operacao', 'produto', 'origem', 'quantidade', 'valor', 'movimentado')
    readonly_fields = ('operacao', 'produto', 'origem', 'quantidade', 'valor',)

@admin.register(CarrinhoProduto)
class CarrinhoProdutoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'carrinho', 'quantidade', 'adicionado',)
    search_fields = ('produto__nome', 'carrinho__id',)
    list_filter = ('adicionado',)

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('carrinho', 'matricula_colaborador', 'data')
    list_filter = ('matricula_colaborador', 'data')
    search_fields = ('carrinho__produto__nome', 'matricula_colaborador')
