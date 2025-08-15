
import random
from django.utils import timezone
from djmoney.money import Money
from djmoney.contrib.exchange.models import Rate, ExchangeBackend

from myapp.models import (
    Cliente, Funcionario, Fornecedor, PecaTipo,
    OfertaFornecedor, ItemVendido
)

def criar_taxa_cambio_usd_para_brl():
    backend, _ = ExchangeBackend.objects.get_or_create(
        name="DatabaseBackend",
        defaults={"base_currency": "USD"}
    )
    Rate.objects.update_or_create(
        backend=backend,
        currency="BRL",
        defaults={"value": 5.25}
    )
    print("Taxa criada com sucesso.")

def popular_banco_de_dados():
    print("Limpando banco de dados...")
    ItemVendido.objects.all().delete()
    OfertaFornecedor.objects.all().delete()
    PecaTipo.objects.all().delete()
    Fornecedor.objects.all().delete()
    Funcionario.objects.all().delete()
    Cliente.objects.all().delete()
    Rate.objects.all().delete()
    ExchangeBackend.objects.all().delete()
    print("Banco limpo com sucesso.")

    criar_taxa_cambio_usd_para_brl()

    print("Criando Clientes...")
    clientes = []
    for i in range(25):
        cliente = Cliente.objects.create(
            nome=f"Cliente {i}",
            email=f"cliente{i}@email.com",
            telefone=f"(11) 9999-00{i:02}",
            endereco=f"Rua Exemplo {i}"
        )
        clientes.append(cliente)

    print("Criando Funcionários...")
    for i in range(25):
        Funcionario.objects.create(
            nome=f"Funcionario {i}",
            email=f"func{i}@empresa.com",
            telefone=f"(11) 9888-00{i:02}",
            cargo="Técnico"
        )

    print("Criando Fornecedores...")
    fornecedores = []
    for i in range(10):
        fornecedor = Fornecedor.objects.create(
            nome=f"Fornecedor {i}",
            email=f"fornecedor{i}@exemplo.com",
            telefone=f"(11) 9777-00{i:02}",
            endereco=f"Av. Fornecedores {i}"
        )
        fornecedores.append(fornecedor)

    print("Criando Tipos de Peças...")
    pecas = []
    for i in range(25):
        peca = PecaTipo.objects.create(
            nome=f"Peça {i}",
            sku=f"SKU-{i:03}",
            descricao=f"Descrição da Peça {i}"
        )
        pecas.append(peca)

    print("Criando Ofertas de Fornecedores...")
    ofertas = []
    for i in range(25):
        peca = random.choice(pecas)
        fornecedor = random.choice(fornecedores)
        try:
            oferta = OfertaFornecedor.objects.create(
                peca_tipo=peca,
                fornecedor=fornecedor,
                preco_custo_usd=Money(random.uniform(50, 200), 'USD')
            )
            ofertas.append(oferta)
        except:
            continue  # Ignora combinações duplicadas

    print("Criando Itens Vendidos...")
    for i in range(25):
        oferta = random.choice(ofertas)
        preco_sugerido = oferta.calcular_preco_venda_sugerido()

        if preco_sugerido is None:
            continue

        cliente = random.choice(clientes)

        ItemVendido.objects.create(
            peca_tipo=oferta.peca_tipo,
            cliente=cliente,
            preco_venda_brl=preco_sugerido,
            data_venda=timezone.now()
        )

    print("População concluída com sucesso.")

if __name__ == "__main__":
    popular_banco_de_dados()
