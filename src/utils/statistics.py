"""
Utilitários para cálculos estatísticos.
"""
from typing import List, Dict, Any
from statistics import mean

from src.models.product import Product, ProductStatistics

def calculate_product_statistics(products: List[Product]) -> ProductStatistics:
    """
    Calcula estatísticas para uma lista de produtos.

    Args:
        products (List[Product]): Lista de produtos

    Returns:
        ProductStatistics: Estatísticas calculadas
    """
    return ProductStatistics.from_products(products)

def prepare_chart_data(products) -> Dict[str, Any]:
    """
    Prepara dados para exibição em gráficos.

    Args:
        products: Lista de produtos (pode ser List[Product] ou lista de dicionários)

    Returns:
        Dict[str, Any]: Dados formatados para gráficos
    """
    if not products:
        return {
            'labels': [],
            'precos': [],
            'media': 0,
            'minimo': 0,
            'maximo': 0
        }

    # Verifica se estamos lidando com objetos Product ou dicionários
    is_dict_format = isinstance(products[0], dict) if products else False

    # Filtra produtos com preços válidos
    if is_dict_format:
        # Formato do agente (dicionários)
        produtos_validos = []
        for p in products:
            # Tenta obter o preço em diferentes formatos
            preco = p.get('preco') or p.get('price') or p.get('preço')
            if preco is not None:
                # Converte string para número se necessário
                if isinstance(preco, str):
                    try:
                        preco = float(preco.replace('R$', '').replace('.', '').replace(',', '.').strip())
                    except ValueError:
                        continue
                if isinstance(preco, (int, float)) and preco > 0:
                    produtos_validos.append(p)
    else:
        # Formato da API (objetos Product)
        produtos_validos = [p for p in products if p.price is not None and isinstance(p.price, (int, float))]

    if not produtos_validos:
        return {
            'labels': [],
            'precos': [],
            'media': 0,
            'minimo': 0,
            'maximo': 0
        }

    # Extrai preços e nomes
    if is_dict_format:
        # Formato do agente
        precos = []
        labels = []
        for p in produtos_validos:
            # Extrai preço
            preco = p.get('preco') or p.get('price') or p.get('preço') or 0
            if isinstance(preco, str):
                preco = float(preco.replace('R$', '').replace('.', '').replace(',', '.').strip())
            precos.append(float(preco))

            # Extrai nome para label
            nome = p.get('titulo') or p.get('name') or p.get('nome') or f"Produto {len(labels)+1}"
            # Limita tamanho do nome
            nome = nome[:20] + '...' if len(nome) > 20 else nome
            labels.append(nome)
    else:
        # Formato da API
        precos = [float(produto.price) for produto in produtos_validos]
        labels = [produto.name[:20] + '...' if produto.name and len(produto.name) > 20 else f"Produto {i+1}"
                 for i, produto in enumerate(produtos_validos)]

    # Calcula estatísticas
    media_precos = mean(precos) if precos else 0
    preco_min = min(precos) if precos else 0
    preco_max = max(precos) if precos else 0

    return {
        'labels': labels,
        'precos': precos,
        'media': float(media_precos),
        'minimo': float(preco_min),
        'maximo': float(preco_max)
    }
