from rest_framework import serializers

from app.models import (Carrinho, Categoria, Estoque, MovimentoEstoque,
                        Produto, Venda)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = (
            'nome',
            'adicionado',
            'atualizado',
        )


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = (
            'nome',
            'preco_custo',
            'preco_venda',
            'categoria',
            'adicionado',
            'atualizado',
        )


class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = (
            'produto',
            'quantidade',
            'adicionado',
            'atualizado',
        )


class MovimentoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentoEstoque
        fields = (
            'produto',
            'quantidade',
            'valor',
            'origem',
            'movimentado',
        )


class CarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrinho
        fields = (
            'usuario',
            'produtos',
        )

    produtos = ProdutoSerializer(many=True)


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = (
            'produto',
            'quantidade',
            'valor',
            'cliente',
            'data',
        )
    