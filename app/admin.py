from django.contrib import admin

from .models import Categoria, Estoque, MovimentoEstoque, Produto, Venda


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'adicionado', 'atualizado',)
    list_display_links = ('nome',)
    search_fields = ('nome', 'adicionado', 'atualizado',)
    list_filter = ('nome', 'adicionado', 'atualizado',)
    list_per_page = 10

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco_custo', 'preco_venda', 'margem_lucro_custo', 'margem_lucro_venda', 'categoria', 'adicionado', 'atualizado',)
    list_display_links = ('nome',)
    search_fields = ('nome', 'preco_custo', 'preco_venda', 'categoria', 'adicionado', 'atualizado',)
    list_filter = ('nome', 'preco_custo', 'preco_venda', 'categoria', 'adicionado', 'atualizado',)
    list_per_page = 20

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'quantidade', 'adicionado', 'atualizado',)
    list_display_links = ('produto',)
    search_fields = ('produto', 'adicionado', 'atualizado',)
    list_filter = ('produto', 'quantidade', 'adicionado', 'atualizado',)
    readonly_fields = ('operacao', 'origem',)
    list_per_page = 10

@admin.register(MovimentoEstoque)
class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'operacao', 'produto', 'origem', 'quantidade', 'valor', 'movimentado')
    list_display_links = ('produto',)
    search_fields = ('operacao', 'produto', 'origem', 'quantidade', 'valor', 'movimentado')
    list_filter = ('operacao', 'produto', 'origem', 'quantidade', 'valor', 'movimentado')
    readonly_fields = ('operacao', 'produto', 'origem', 'quantidade', 'valor',)
    list_per_page = 20

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'quantidade', 'valor', 'matricula_colaborador', 'data')
    list_display_links = ('produto',)
    search_fields = ('produto', 'quantidade', 'matricula_colaborador', 'data')
    list_filter = ('produto', 'quantidade', 'matricula_colaborador', 'data')
    readonly_fields = ('produto', 'quantidade', 'valor', 'matricula_colaborador', 'data')
