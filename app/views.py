from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from .forms import CustomUserCreationForm
from .models import Carrinho, CarrinhoProduto, Estoque, Produto, Venda


def register(request):
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()  # Salva o usuário no banco de dados
            username = formulario.cleaned_data.get('username')
            password = formulario.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('lista_produtos')  # Redireciona para a página desejada após o login
    else:
        formulario = CustomUserCreationForm()

    return render(request, 'templates/app/pages/registro.html', {'formulario': formulario})    
    

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.POST.get('username') == request.user.username:
            raise Http404()
        
        logout(request) 
        return redirect('login')


@method_decorator(login_required, name='dispatch')
class ListaProdutoView(View):
    def get(self, request):
        produtos = Produto.objects.all()
        usuario = request.user.username
        
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

        # Calcula o total de itens e o valor total do carrinho
        try:
            carrinho = Carrinho.objects.get(usuario=request.user)
            produtos_no_carrinho = CarrinhoProduto.objects.filter(carrinho=carrinho)

            if produtos_no_carrinho.exists():
                itens_carrinho = sum(item.quantidade for item in produtos_no_carrinho)
                valor_carrinho = sum(float(item.valor) for item in produtos_no_carrinho)
            else:
                itens_carrinho = 0
                valor_carrinho = 0.0

        except Carrinho.DoesNotExist:
            itens_carrinho = 0
            valor_carrinho = 0.0
        
        return render(request, 'templates/app/pages/lista_produtos.html', {
            'produtos_com_estoque': produtos_com_estoque, 
            'usuario': usuario,
            'itens_carrinho': itens_carrinho,
            'valor_carrinho': valor_carrinho,
        })  


@method_decorator(login_required, name='dispatch')
class FiltraView(View):
    def get(self, request):
        filtro = request.GET.get('q', '').strip()
        usuario = request.user.username

        if not filtro:
            raise Http404()

        produtos = Produto.objects.filter(
            Q(
                Q(nome__icontains=filtro) |
                Q(descricao__icontains=filtro) |
                Q(codigo_barra__icontains=filtro),
            ),
        ).order_by('nome')

        estoques = Estoque.objects.filter(produto__in=produtos)

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
        
        # Calcula o total de itens e o valor total do carrinho
        try:
            carrinho = Carrinho.objects.get(usuario=request.user)
            produtos_no_carrinho = CarrinhoProduto.objects.filter(carrinho=carrinho)

            if produtos_no_carrinho.exists():
                itens_carrinho = sum(item.quantidade for item in produtos_no_carrinho)
                valor_carrinho = sum(float(item.valor) for item in produtos_no_carrinho)
            else:
                itens_carrinho = 0
                valor_carrinho = 0.0

        except Carrinho.DoesNotExist:
            itens_carrinho = 0
            valor_carrinho = 0.0
        
        return render(request, 'templates/app/pages/lista_produtos.html', {
            'produtos_com_estoque': produtos_com_estoque, 
            'usuario': usuario,
            'itens_carrinho': itens_carrinho,
            'valor_carrinho': valor_carrinho,
        })  


@method_decorator(login_required, name='dispatch')
class AdicionaCarrinhoView(View):
    def post(self, request, produto_id):
        produto = get_object_or_404(Produto, id=produto_id)
        quantidade = int(request.POST.get('quantidade', 1))
        estoque = get_object_or_404(Estoque, produto=produto)

        if estoque.quantidade < quantidade:
            # Aqui você pode adicionar uma mensagem de erro ao invés de apenas redirecionar
            return redirect('lista_produtos')

        carrinho_id = request.session.get('carrinho_id')
        carrinho = None

        if not carrinho_id:
            # Verifica se o usuário já possui um carrinho antes de criar um novo
            try:
                carrinho = Carrinho.objects.get(usuario=request.user)
            except Carrinho.DoesNotExist:
                carrinho = Carrinho.objects.create(usuario=request.user)
            # Armazena o carrinho na sessão
            request.session['carrinho_id'] = carrinho.id
        else:
            try:
                carrinho = Carrinho.objects.get(id=carrinho_id)
                # Garantir que o carrinho pertence ao usuário logado
                if carrinho.usuario != request.user:
                    carrinho = Carrinho.objects.get(usuario=request.user)
                    request.session['carrinho_id'] = carrinho.id
            except Carrinho.DoesNotExist:
                carrinho = Carrinho.objects.get_or_create(usuario=request.user)[0]
                request.session['carrinho_id'] = carrinho.id

        with transaction.atomic():
            carrinho_produto, created = CarrinhoProduto.objects.get_or_create(carrinho=carrinho, produto=produto)
            
            carrinho_produto.quantidade = F('quantidade') + quantidade
            carrinho_produto.valor = F('valor') + (produto.preco_venda * quantidade)
            carrinho_produto.adicionado = timezone.now()
            carrinho_produto.save()

            estoque.quantidade -= quantidade
            estoque.operacao = 'saida'
            estoque.origem = 'entrada_carrinho'
            estoque.save()

        return redirect('ver_carrinho')
    

@method_decorator(login_required, name='dispatch')
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
        
        with transaction.atomic():
            # Decrementa a quantidade e valor do produto no carrinho
            carrinho_produto.quantidade -= 1 
            carrinho_produto.valor -= produto.preco_venda 
            
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


@method_decorator(login_required, name='dispatch')
class LimpaCarrinhoView(View):
    def get(self, request):
        carrinho_id = request.session.get('carrinho_id')
        
        if not carrinho_id:
            return redirect('ver_carrinho')  # Se não há carrinho, redirecionar para ver carrinho

        try:
            carrinho = Carrinho.objects.get(id=carrinho_id)
        except Carrinho.DoesNotExist:
            return redirect('ver_carrinho')  # Se o carrinho não existe, redirecionar para ver carrinho

        carrinho_produtos = CarrinhoProduto.objects.filter(carrinho=carrinho)
        
        with transaction.atomic():
            for item in carrinho_produtos:
                # Atualiza o estoque
                estoque = get_object_or_404(Estoque, produto=item.produto)
                estoque.quantidade += item.quantidade
                estoque.operacao = 'entrada'
                estoque.origem = 'estorno_carrinho'
                estoque.save()
            
            # Limpa o carrinho
            carrinho_produtos.delete()

        return redirect('ver_carrinho')


@method_decorator(login_required, name='dispatch')
class VerCarrinhoView(View):
    def get(self, request):
        try:
            carrinho = Carrinho.objects.get(usuario=request.user)
        except Carrinho.DoesNotExist:
            return render(request, 'templates/app/pages/carrinho_vazio.html')

        produtos_no_carrinho = CarrinhoProduto.objects.filter(carrinho=carrinho)

        if not produtos_no_carrinho.exists():
            return render(request, 'templates/app/pages/carrinho_vazio.html')

        itens = 0
        valor_total = 0.0
        for item in produtos_no_carrinho:
            itens += item.quantidade
            valor_total += float(item.valor)

        return render(request, 'templates/app/pages/ver_carrinho.html', {'produtos_no_carrinho': produtos_no_carrinho, 'itens': itens, 'valor_total': f'{valor_total:.2f}'})
    

@method_decorator(login_required, name='dispatch')
class PagamentoView(View):
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
        
        return render(request, 'templates/app/pages/pagamento.html', {'itens': itens, 'valor_total': valor_total})

    
@method_decorator(login_required, name='dispatch')    
class FinalizarCompraView(View):
    def get(self, request):
        carrinho_id = request.session.get('carrinho_id')
        
        if not carrinho_id:
            return redirect('ver_carrinho')
        
        try:
            carrinho = Carrinho.objects.get(id=carrinho_id)
        except Carrinho.DoesNotExist:
            return redirect('ver_carrinho')
        
        produtos_no_carrinho = CarrinhoProduto.objects.filter(carrinho=carrinho)

        if not produtos_no_carrinho.exists():
            return redirect('ver_carrinho')

        with transaction.atomic():
            for item in produtos_no_carrinho:
                # Criar instância de Venda
                Venda.objects.create(
                    produto=item.produto,
                    quantidade=item.quantidade,
                    valor=item.valor,
                    cliente=request.user.username,
                    data=timezone.now()
                )

            Carrinho.objects.filter(id=carrinho_id).delete()
            request.session['carrinho_id'] = None

        return render(request, 'templates/app/pages/compra_finalizada.html')