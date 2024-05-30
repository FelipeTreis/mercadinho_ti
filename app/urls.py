from django.urls import include, path

from .views import (AdicionaCarrinhoView, FinalizarCompraView,
                    ListaProdutoView, RemoveCarrinhoView, VerCarrinhoView)

urlpatterns = [
    path('', ListaProdutoView.as_view(), name='lista_produtos'),
    path('adicionar/<int:produto_id>/', AdicionaCarrinhoView.as_view(), name='adicionar_ao_carrinho'),
    path('remover/<int:produto_id>/', RemoveCarrinhoView.as_view(), name='remove_do_carrinho'),
    path('carrinho/', VerCarrinhoView.as_view(), name='ver_carrinho'),
    path('finalizar', FinalizarCompraView.as_view(), name='finalizar_compra'),
]

