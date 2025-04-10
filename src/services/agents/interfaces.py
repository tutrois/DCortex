"""
Interfaces para agentes de processamento.
Define contratos que as implementações concretas de agentes devem seguir.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

class AgentInterface(ABC):
    """Interface base para todos os agentes."""
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Processa os dados de entrada e retorna o resultado.
        
        Args:
            input_data (Any): Dados de entrada para processamento
            
        Returns:
            Any: Resultado do processamento
        """
        pass
    
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """
        Retorna o tipo do agente.
        
        Returns:
            str: Tipo do agente
        """
        pass
    
    @property
    @abstractmethod
    def agent_name(self) -> str:
        """
        Retorna o nome do agente.
        
        Returns:
            str: Nome do agente
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """
        Retorna a descrição do agente.
        
        Returns:
            str: Descrição do agente
        """
        pass

class DataFetcherAgentInterface(AgentInterface):
    """Interface para agentes que buscam dados externos."""
    
    @abstractmethod
    def fetch_data(self, source: str) -> Optional[str]:
        """
        Busca dados de uma fonte externa.
        
        Args:
            source (str): Fonte dos dados (URL, caminho de arquivo, etc.)
            
        Returns:
            Optional[str]: Dados obtidos ou None em caso de erro
        """
        pass

class DataProcessorAgentInterface(AgentInterface):
    """Interface para agentes que processam dados."""
    
    @abstractmethod
    def process_data(self, data: str) -> Union[List[Dict[str, Any]], None]:
        """
        Processa dados brutos e retorna uma estrutura de dados organizada.
        
        Args:
            data (str): Dados brutos a serem processados
            
        Returns:
            Union[List[Dict[str, Any]], None]: Lista de dicionários com dados processados ou None em caso de erro
        """
        pass
