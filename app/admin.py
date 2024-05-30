from django.contrib import admin

from .models import CarrinhoProduto, Categoria, Estoque, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'adicionado', 'atualizado',)
    search_fields = ('nome',)
    list_filter = ('adicionado', 'atualizado',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'categoria', 'adicionado', 'atualizado',)
    search_fields = ('nome', 'descricao',)
    list_filter = ('categoria', 'adicionado', 'atualizado',)

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'quantidade', 'adicionado', 'atualizado',)
    search_fields = ('produto__nome',)
    list_editable = ('quantidade',)
    list_filter = ('adicionado', 'atualizado',)

@admin.register(CarrinhoProduto)
class CarrinhoProdutoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'carrinho', 'quantidade', 'adicionado',)
    search_fields = ('produto__nome', 'carrinho__id',)
    list_filter = ('adicionado',)
