"""
Serviço de orquestração de agentes.
Coordena a execução de múltiplos agentes para realizar tarefas complexas.
"""
from typing import Any, Dict, List, Optional, Union

from src.config.agents import get_agent_config
from src.models.product import Product
from src.services.agents.interfaces import DataFetcherAgentInterface, DataProcessorAgentInterface
from src.services.agents.registry import AgentFactory
from src.utils.logging import get_logger

logger = get_logger(__name__)

class AgentOrchestrator:
    """
    Orquestrador de agentes.
    Coordena a execução de múltiplos agentes para realizar tarefas complexas.
    """
    
    def __init__(self):
        """
        Inicializa o orquestrador de agentes.
        """
        self.agent_config = get_agent_config()
        self.factory = AgentFactory()
        logger.info("Orquestrador de agentes inicializado")
    
    def fetch_and_process_data(self, source: str, 
                               fetcher_type: Optional[str] = None, 
                               processor_type: Optional[str] = None) -> Union[List[Dict[str, Any]], None]:
        """
        Busca e processa dados usando os agentes especificados.
        
        Args:
            source (str): Fonte dos dados
            fetcher_type (Optional[str]): Tipo do agente de busca. Se None, usa o padrão.
            processor_type (Optional[str]): Tipo do agente de processamento. Se None, usa o padrão.
            
        Returns:
            Union[List[Dict[str, Any]], None]: Dados processados ou None em caso de erro
        """
        # Determina os tipos de agentes a serem usados
        fetcher_type = fetcher_type or self.agent_config["default_fetcher"]
        processor_type = processor_type or self.agent_config["default_processor"]
        
        logger.info(f"Usando agente de busca: {fetcher_type}")
        logger.info(f"Usando agente de processamento: {processor_type}")
        
        # Cria os agentes
        fetcher = self.factory.create_agent(fetcher_type)
        processor = self.factory.create_agent(processor_type)
        
        if not fetcher or not isinstance(fetcher, DataFetcherAgentInterface):
            logger.error(f"Agente de busca '{fetcher_type}' não encontrado ou inválido")
            return None
        
        if not processor or not isinstance(processor, DataProcessorAgentInterface):
            logger.error(f"Agente de processamento '{processor_type}' não encontrado ou inválido")
            return None
        
        # Executa a busca
        raw_data = fetcher.fetch_data(source)
        if not raw_data:
            logger.error("Falha ao buscar dados")
            return None
        
        # Processa os dados
        processed_data = processor.process_data(raw_data)
        if not processed_data:
            logger.error("Falha ao processar dados")
            return None
        
        return processed_data
    
    def fetch_and_process_products(self, source: str,
                                  fetcher_type: Optional[str] = None,
                                  processor_type: Optional[str] = None) -> List[Product]:
        """
        Busca e processa produtos usando os agentes especificados.
        
        Args:
            source (str): Fonte dos dados
            fetcher_type (Optional[str]): Tipo do agente de busca. Se None, usa o padrão.
            processor_type (Optional[str]): Tipo do agente de processamento. Se None, usa o padrão.
            
        Returns:
            List[Product]: Lista de produtos processados
        """
        # Busca e processa os dados
        products_data = self.fetch_and_process_data(source, fetcher_type, processor_type)
        
        if not products_data:
            logger.error("Nenhum produto encontrado")
            return []
        
        # Converte para objetos Product
        products = [Product.from_dict(product) for product in products_data]
        logger.info(f"Processados {len(products)} produtos")
        
        return products
    
    def list_available_agents(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Lista os agentes disponíveis por tipo.
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: Dicionário com agentes por tipo
        """
        return self.agent_config["available_agents"]
