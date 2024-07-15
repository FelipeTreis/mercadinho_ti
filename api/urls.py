from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.viewsets import (CarrinhoViewSet, CategoriaViewSet, EstoqueViewSet,
                          MovimentoEstoqueViewSet, ProdutoViewSet,
                          VendaViewSet)

app_name = 'api'

router = SimpleRouter()
router.register('categoria', CategoriaViewSet, basename='categoria')
router.register('produto', ProdutoViewSet, basename='produto')
router.register('estoque', EstoqueViewSet, basename='estoque')
router.register('movimeto-estoque', MovimentoEstoqueViewSet, basename='movimeto_estoque')
router.register('carrinho', CarrinhoViewSet, basename='carrinho')
router.register('venda', VendaViewSet, basename='venda')

urlpatterns = [
    path('', include(router.urls)),
]
