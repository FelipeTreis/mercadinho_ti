from django.urls import include, path

from .views import (AdicionaCarrinhoView, FiltraView, FinalizarCompraView,
                    ListaProdutoView, PagamentoView, RemoveCarrinhoView,
                    VerCarrinhoView)

urlpatterns = [
    path('', ListaProdutoView.as_view(), name='lista_produtos'),
    path('filtrar/', FiltraView.as_view(), name='filtrar'),
    path('adicionar/<int:produto_id>/', AdicionaCarrinhoView.as_view(), name='adicionar_ao_carrinho'),
    path('remover/<int:produto_id>/', RemoveCarrinhoView.as_view(), name='remove_do_carrinho'),
    path('carrinho/', VerCarrinhoView.as_view(), name='ver_carrinho'),
    path('pagamento/', PagamentoView.as_view(), name='pagamento'),
    path('compra-finalizada/', FinalizarCompraView.as_view(), name='compra_finalizada'),
]

