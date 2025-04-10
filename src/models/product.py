"""
Módulo que define os modelos de dados para produtos.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class Product:
    """
    Modelo de dados para representar um produto.
    
    Attributes:
        name (str): Nome do produto
        price (float): Preço do produto
        rating (Optional[float]): Avaliação do produto (0-5 estrelas)
        image_url (Optional[str]): URL da imagem do produto
        url (Optional[str]): URL da página do produto
        description (Optional[str]): Descrição do produto
    """
    name: str
    price: float
    rating: Optional[float] = None
    image_url: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """
        Cria uma instância de Product a partir de um dicionário.
        
        Args:
            data (Dict[str, Any]): Dicionário com os dados do produto
            
        Returns:
            Product: Instância de Product
        """
        return cls(
            name=data.get('titulo', ''),
            price=float(data.get('preco', 0.0)),
            rating=float(data.get('rating', 0.0)) if data.get('rating') else None,
            image_url=data.get('imagem', None),
            url=data.get('url_produto', None),
            description=data.get('descricao', None)
        )

@dataclass
class ProductStatistics:
    """
    Estatísticas calculadas para um conjunto de produtos.
    
    Attributes:
        average_price (float): Preço médio
        min_price (float): Preço mínimo
        max_price (float): Preço máximo
        product_count (int): Número de produtos
    """
    average_price: float
    min_price: float
    max_price: float
    product_count: int
    
    @classmethod
    def from_products(cls, products: List[Product]) -> 'ProductStatistics':
        """
        Calcula estatísticas a partir de uma lista de produtos.
        
        Args:
            products (List[Product]): Lista de produtos
            
        Returns:
            ProductStatistics: Estatísticas calculadas
        """
        if not products:
            return cls(0.0, 0.0, 0.0, 0)
            
        prices = [product.price for product in products]
        return cls(
            average_price=sum(prices) / len(prices),
            min_price=min(prices),
            max_price=max(prices),
            product_count=len(products)
        )
