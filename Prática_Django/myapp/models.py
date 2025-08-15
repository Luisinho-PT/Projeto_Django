from django.db import models
from djmoney.models.fields import MoneyField

# Tenta importar 'convert_money' do local mais recente, e usa o antigo como fallback
try:
    from djmoney.money import convert_money
except ImportError:
    from djmoney.contrib.exchange.models import convert_money

# --- Modelos de Entidades ---

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=50)
    data_admissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# --- Modelos de Catálogo e Ofertas ---

class PecaTipo(models.Model):
    """Representa um tipo de peça no catálogo, ex: 'Tela iPhone 15'."""
    nome = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True, help_text="Código único da peça, ex: AP-IP15-TELA")
    descricao = models.TextField(blank=True, null=True)
    
    fornecedores = models.ManyToManyField(
        Fornecedor,
        through='OfertaFornecedor',
        related_name='pecas_oferecidas'
    )

    def __str__(self):
        return f"{self.nome} (SKU: {self.sku})"

class OfertaFornecedor(models.Model):
    """Modela o preço de CUSTO (USD) de um tipo de peça por um fornecedor."""
    peca_tipo = models.ForeignKey(PecaTipo, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    
    preco_custo_usd = MoneyField(
        max_digits=14, decimal_places=2, default_currency='USD'
    )
    data_atualizacao_preco = models.DateTimeField(auto_now=True)

    def calcular_preco_venda_sugerido(self, margem_percentual=80):
        """
        Converte o custo para BRL e aplica uma margem de lucro.
        Retorna um objeto Money em BRL.
        """
        try:
            custo_em_brl = convert_money(self.preco_custo_usd, 'BRL')
            valor_da_margem = custo_em_brl * margem_percentual / 100
            preco_sugerido = custo_em_brl + valor_da_margem
            return preco_sugerido
        except Exception as e:
            print(f"Não foi possível converter a moeda: {e}")
            return None

    class Meta:
        unique_together = ('peca_tipo', 'fornecedor')

    def __str__(self):
        return f"{self.fornecedor.nome} oferece {self.peca_tipo.nome} por {self.preco_custo_usd}"

# --- Modelo de Transação / Venda ---

class ItemVendido(models.Model):
    """Representa uma peça específica que foi vendida a um cliente."""
    peca_tipo = models.ForeignKey(PecaTipo, on_delete=models.PROTECT, help_text="O tipo de peça do catálogo que foi vendido.")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='itens_comprados')
    
    preco_venda_brl = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='BRL',
        help_text="Preço final de venda para o cliente em Reais."
    )
    data_venda = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.peca_tipo.nome} vendido para {self.cliente.nome} por {self.preco_venda_brl}"
