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

def prepare_chart_data(products: List[Product]) -> Dict[str, Any]:
    """
    Prepara dados para exibição em gráficos.

    Args:
        products (List[Product]): Lista de produtos

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

    # Filtra produtos com preços válidos
    produtos_validos = [p for p in products if p.price is not None and isinstance(p.price, (int, float))]

    if not produtos_validos:
        return {
            'labels': [],
            'precos': [],
            'media': 0,
            'minimo': 0,
            'maximo': 0
        }

    # Converte para float para garantir que são números válidos
    precos = [float(produto.price) for produto in produtos_validos]
    media_precos = mean(precos)
    preco_min = min(precos)
    preco_max = max(precos)

    return {
        'labels': [f"Produto {i+1}" for i in range(len(produtos_validos))],
        'precos': precos,
        'media': float(media_precos),
        'minimo': float(preco_min),
        'maximo': float(preco_max)
    }
