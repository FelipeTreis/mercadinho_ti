from django.db import models

OPERACAO = (
    ('entrada', 'entrada'),
    ('saida', 'saida'),
)

ORIGEM = (
    ('compra', 'compra'),
    ('venda', 'venda'),
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
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barra = models.CharField(max_length=255, unique=True)    
    categoria = models.ForeignKey(Categoria, related_name='categorias', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/')
    adicionado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    produto = models.ForeignKey(Produto, related_name='estoques', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    adicionado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
    
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
        return f'{self.quantidade} x {self.produto.nome}'
    

class Venda(models.Model):
    carrinho = models.ForeignKey(CarrinhoProduto, on_delete=models.CASCADE)    
    matricula_colaborador = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.matricula_colaborador} - {self.carrinho.produto} - {self.carrinho.quantidade} un. - R${self.carrinho.valor}'
