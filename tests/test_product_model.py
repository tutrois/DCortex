"""
Testes para o modelo Product.
"""
import pytest
from src.models.product import Product, ProductStatistics

def test_product_creation():
    """Testa a criação de um produto."""
    product = Product(name="Test Product", price=99.99)
    
    assert product.name == "Test Product"
    assert product.price == 99.99
    assert product.rating is None
    assert product.image_url is None
    assert product.url is None
    assert product.description is None

def test_product_from_dict():
    """Testa a criação de um produto a partir de um dicionário."""
    data = {
        "nome": "Test Product",
        "preço": 99.99,
        "avaliação": 4.5,
        "imagem": "http://example.com/image.jpg",
        "url": "http://example.com/product",
        "descrição": "A test product"
    }
    
    product = Product.from_dict(data)
    
    assert product.name == "Test Product"
    assert product.price == 99.99
    assert product.rating == 4.5
    assert product.image_url == "http://example.com/image.jpg"
    assert product.url == "http://example.com/product"
    assert product.description == "A test product"

def test_product_statistics():
    """Testa o cálculo de estatísticas de produtos."""
    products = [
        Product(name="Product 1", price=10.0),
        Product(name="Product 2", price=20.0),
        Product(name="Product 3", price=30.0)
    ]
    
    stats = ProductStatistics.from_products(products)
    
    assert stats.average_price == 20.0
    assert stats.min_price == 10.0
    assert stats.max_price == 30.0
    assert stats.product_count == 3

def test_product_statistics_empty():
    """Testa o cálculo de estatísticas com lista vazia."""
    stats = ProductStatistics.from_products([])
    
    assert stats.average_price == 0.0
    assert stats.min_price == 0.0
    assert stats.max_price == 0.0
    assert stats.product_count == 0
