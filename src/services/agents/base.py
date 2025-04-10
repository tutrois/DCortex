"""
Classes base para implementações de agentes.
"""
from abc import ABC
from typing import Any, Dict, List, Optional, Union

from src.services.agents.interfaces import AgentInterface, DataFetcherAgentInterface, DataProcessorAgentInterface
from src.utils.logging import get_logger

logger = get_logger(__name__)

class BaseAgent(AgentInterface, ABC):
    """
    Classe base para todos os agentes.
    Implementa funcionalidades comuns a todos os agentes.
    """
    
    def __init__(self, name: str, agent_type: str, description: str):
        """
        Inicializa um agente base.
        
        Args:
            name (str): Nome do agente
            agent_type (str): Tipo do agente
            description (str): Descrição do agente
        """
        self._name = name
        self._type = agent_type
        self._description = description
        logger.info(f"Agente {name} ({agent_type}) inicializado")
    
    @property
    def agent_name(self) -> str:
        """
        Retorna o nome do agente.
        
        Returns:
            str: Nome do agente
        """
        return self._name
    
    @property
    def agent_type(self) -> str:
        """
        Retorna o tipo do agente.
        
        Returns:
            str: Tipo do agente
        """
        return self._type
    
    @property
    def description(self) -> str:
        """
        Retorna a descrição do agente.
        
        Returns:
            str: Descrição do agente
        """
        return self._description

class BaseDataFetcherAgent(BaseAgent, DataFetcherAgentInterface, ABC):
    """
    Classe base para agentes que buscam dados.
    """
    
    def __init__(self, name: str, description: str):
        """
        Inicializa um agente de busca de dados.
        
        Args:
            name (str): Nome do agente
            description (str): Descrição do agente
        """
        super().__init__(name, "data_fetcher", description)
    
    def process(self, input_data: Any) -> Any:
        """
        Implementação padrão do método process para agentes de busca.
        
        Args:
            input_data (Any): Dados de entrada (normalmente uma URL ou fonte)
            
        Returns:
            Any: Resultado da busca
        """
        if isinstance(input_data, str):
            return self.fetch_data(input_data)
        else:
            logger.error(f"Entrada inválida para agente {self.agent_name}. Esperado string, recebido {type(input_data)}")
            return None

class BaseDataProcessorAgent(BaseAgent, DataProcessorAgentInterface, ABC):
    """
    Classe base para agentes que processam dados.
    """
    
    def __init__(self, name: str, description: str):
        """
        Inicializa um agente de processamento de dados.
        
        Args:
            name (str): Nome do agente
            description (str): Descrição do agente
        """
        super().__init__(name, "data_processor", description)
    
    def process(self, input_data: Any) -> Any:
        """
        Implementação padrão do método process para agentes de processamento.
        
        Args:
            input_data (Any): Dados de entrada para processamento
            
        Returns:
            Any: Resultado do processamento
        """
        if isinstance(input_data, str):
            return self.process_data(input_data)
        else:
            logger.error(f"Entrada inválida para agente {self.agent_name}. Esperado string, recebido {type(input_data)}")
            return None
