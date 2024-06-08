from decimal import Decimal

from django.db import models
from django.utils import timezone
from django_lifecycle import AFTER_CREATE, AFTER_UPDATE, LifecycleModel, hook

OPERACAO = (
    ('entrada', 'entrada'),
    ('saida', 'saida'),
)

ORIGEM = (
    ('compra', 'compra'),
    ('venda', 'venda'),
    ('entrada_carrinho', 'entrada_carrinho'),
    ('estorno_carrinho', 'estorno_carrinho'),
)


class Categoria(models.Model):
    nome = models.CharField(max_length=60, unique=True)
    adicionado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=60, unique=True)
    descricao = models.TextField()
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barra = models.CharField(max_length=255, unique=True)    
    categoria = models.ForeignKey(Categoria, related_name='categorias', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/')
    adicionado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    @property
    def margem_lucro_custo(self):
        lucro_bruto = self.preco_venda - self.preco_custo
        margem = (lucro_bruto / self.preco_custo) * 100

        return f'{margem:.2f}%'
    
    @property
    def margem_lucro_venda(self):
        lucro_bruto = self.preco_venda - self.preco_custo
        margem = (lucro_bruto / self.preco_venda) * 100

        return f'{margem:.2f}%'

    def __str__(self):
        return self.nome


class Estoque(LifecycleModel):
    produto = models.OneToOneField(Produto, related_name='estoques', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    adicionado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
    operacao = models.CharField(default='entrada', max_length=10, null=False, blank=False)
    origem = models.CharField(default='compra', max_length=20, null=False, blank=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_quantidade = self.quantidade
        self.operacao = 'entrada'
        self.origem = 'compra'

    @hook(AFTER_CREATE)
    def cria_movimento_entrada_criacao(self):
        MovimentoEstoque.objects.create(
            produto=self.produto,
            quantidade=self.quantidade,
            valor=self.produto.preco_venda * self.quantidade,
            operacao='entrada',
            origem='compra',
            movimentado=timezone.now()
        )

    @hook(AFTER_UPDATE, when='quantidade')
    def cria_movimento_entrada_atualizacao(self):
        quantidade_diferenca = self.quantidade - self._original_quantidade
        if quantidade_diferenca != 0:
            if (self.operacao == 'entrada' and self.origem == 'compra') or (self.operacao == 'saida' and self.origem == 'entrada_carrinho') or (self.operacao == 'entrada' and self.origem == 'estorno_carrinho'):
                MovimentoEstoque.objects.create(
                    produto = self.produto,
                    quantidade = abs(quantidade_diferenca),
                    valor=self.produto.preco_venda * abs(quantidade_diferenca),
                    operacao = self.operacao,
                    origem = self.origem,
                    movimentado = timezone.now()
                )

        self._original_quantidade = self.quantidade
        self.origem_atualizacao = None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._original_quantidade = self.quantidade
        self.operacao = 'entrada'
        self.origem = 'compra'

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade} unidade(s)'
    

class MovimentoEstoque(models.Model):
    produto = models.ForeignKey(Produto, related_name='movimentos_estoques', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=False, blank=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    operacao = models.CharField(choices=OPERACAO, max_length=10, null=False, blank=False)
    origem = models.CharField(choices=ORIGEM, max_length=20, null=False, blank=False)
    movimentado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.operacao} - {self.produto.nome} - {self.quantidade} unidade(s)'
    

class Carrinho(models.Model):
    produtos = models.ManyToManyField(Produto, through='CarrinhoProduto')    


class CarrinhoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade} unidade(s) - R${self.valor}'
    

class Venda(LifecycleModel):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=False, blank=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    matricula_colaborador = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    @hook(AFTER_CREATE)
    def cria_movimento_saida(self):
        MovimentoEstoque.objects.create(
            produto = self.produto,
            quantidade = self.quantidade,
            valor = self.valor,
            operacao = 'saida',
            origem = 'venda',
            movimentado = timezone.now()
        )

    def __str__(self):
        return f'{self.matricula_colaborador} - {self.produto} - {self.quantidade} un. - R${self.valor}'
