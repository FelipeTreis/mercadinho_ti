from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (AdicionaCarrinhoView, FiltraView, FinalizarCompraView,
                    LimpaCarrinhoView, ListaProdutoView, LogoutView,
                    PagamentoView, RemoveCarrinhoView, VerCarrinhoView,
                    register)

urlpatterns = [
    path('', ListaProdutoView.as_view(), name='lista_produtos'),
    path('filtrar/', FiltraView.as_view(), name='filtrar'),
    path('adicionar/<int:produto_id>/', AdicionaCarrinhoView.as_view(), name='adicionar_ao_carrinho'),
    path('remover/<int:produto_id>/', RemoveCarrinhoView.as_view(), name='remove_do_carrinho'),
    path('limpar-carrinho/', LimpaCarrinhoView.as_view(), name='limpa_carrinho'),
    path('carrinho/', VerCarrinhoView.as_view(), name='ver_carrinho'),
    path('pagamento/', PagamentoView.as_view(), name='pagamento'),
    path('compra-finalizada/', FinalizarCompraView.as_view(), name='compra_finalizada'),
    
    #Rotas referentes ao usuário
    path('login/', auth_views.LoginView.as_view(template_name='templates/app/pages/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', register, name='registro'),
]

