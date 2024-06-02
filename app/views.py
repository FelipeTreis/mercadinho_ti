from decimal import Decimal

from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from .models import Carrinho, CarrinhoProduto, Estoque, Produto


class ListaProdutoView(View):
    def get(self, request):
        produtos = Produto.objects.all()
        
        # Filtra os estoques dos produtos
        estoques = Estoque.objects.filter(produto__in=produtos)
        
        # Lista para armazenar os produtos com estoque e suas quantidades
        produtos_com_estoque = []
        
        for produto in produtos:
            # Verifica se existe estoque para o produto
            estoque_produto = estoques.filter(produto=produto).first()
            if estoque_produto:
                quantidade = estoque_produto.quantidade
                # Verifica se a quantidade em estoque é zero
                if quantidade == 0:
                    # Atualiza a disponibilidade do produto para False
                    produto.disponivel = False
                    produto.save()
            else:
                quantidade = 0
                
            produtos_com_estoque.append({
                'produto': produto,
                'quantidade': quantidade
            })
        
        return render(request, 'templates/app/pages/lista_produtos.html', {'produtos_com_estoque': produtos_com_estoque})  


class AdicionaCarrinhoView(View):
    def get(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id)
        estoque = get_object_or_404(Estoque, produto=produto)

        if estoque.quantidade <= 0:
            return redirect('lista_produtos')

        carrinho_id = request.session.get('carrinho_id')
        carrinho = None

        if not carrinho_id: 
            carrinho = Carrinho.objects.create()
            request.session['carrinho_id'] = carrinho.id
        else:
            try:
                carrinho = Carrinho.objects.get(id=carrinho_id)
            except Carrinho.DoesNotExist:
                carrinho = Carrinho.objects.create()
                request.session['carrinho_id'] = carrinho.id

        carrinho_produto, created = CarrinhoProduto.objects.get_or_create(carrinho=carrinho, produto=produto)
        
        carrinho_produto.quantidade += 1
        carrinho_produto.valor += produto.preco
        carrinho_produto.adicionado = timezone.now()
        carrinho_produto.save()

        estoque.quantidade -= 1
        estoque.operacao = 'saida'
        estoque.origem = 'entrada_carrinho'
        estoque.save()

        return redirect('ver_carrinho')
    

class RemoveCarrinhoView(View):
    def get(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho_id = request.session.get('carrinho_id')
        
        if not carrinho_id:
            return redirect('ver_carrinho')  # Se não há carrinho, redirecionar para ver carrinho

        try:
            carrinho = Carrinho.objects.get(id=carrinho_id)
        except Carrinho.DoesNotExist:
            return redirect('ver_carrinho')  # Se o carrinho não existe, redirecionar para ver carrinho

        try:
            carrinho_produto = CarrinhoProduto.objects.get(carrinho=carrinho, produto=produto)
        except CarrinhoProduto.DoesNotExist:
            return redirect('ver_carrinho')  # Se o produto não está no carrinho, redirecionar para ver carrinho
        
        # Decrementa a quantidade e valor do produto no carrinho
        carrinho_produto.quantidade -= 1
        carrinho_produto.valor -= produto.preco
        
        # Atualiza o tempo de adição
        carrinho_produto.adicionado = timezone.now()

        # Se a quantidade for zero, remove o item do carrinho
        if carrinho_produto.quantidade <= 0:
            carrinho_produto.delete()
        else:
            carrinho_produto.save()

        # Reabastece o estoque
        estoque = get_object_or_404(Estoque, produto=produto)
        estoque.quantidade += 1
        estoque.operacao = 'entrada'
        estoque.origem = 'estorno_carrinho'
        estoque.save()

        return redirect('ver_carrinho')


class VerCarrinhoView(View):
    def get(self, request):
        carrinho_id = request.session.get('carrinho_id')
        if not carrinho_id:
            return render(request, 'templates/app/pages/carrinho_vazio.html')
        
        try:
            carrinho = Carrinho.objects.get(id=carrinho_id)
        except Carrinho.DoesNotExist:
            return render(request, 'templates/app/pages/carrinho_vazio.html')

        produtos_no_carrinho = CarrinhoProduto.objects.filter(carrinho=carrinho)

        if not produtos_no_carrinho.exists():
            return render(request, 'templates/app/pages/carrinho_vazio.html')
        
        itens = 0
        valor_total = Decimal('0.00')

        for item in produtos_no_carrinho:
            itens += item.quantidade 
            valor_total += item.valor 
        
        return render(request, 'templates/app/pages/ver_carrinho.html', {'produtos_no_carrinho': produtos_no_carrinho, 'itens': itens, 'valor_total': valor_total})

    
class FinalizarCompraView(View):
    def get(self, request):
        carrinho_id = request.session.get('carrinho_id')
        if carrinho_id:
            Carrinho.objects.filter(id=carrinho_id).delete()
            request.session['carrinho_id'] = None
        return render(request, 'templates/app/pages/compra_finalizada.html')