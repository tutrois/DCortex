"""
Registro e fábrica de agentes.
Permite registrar, recuperar e criar instâncias de diferentes tipos de agentes.
"""
from typing import Dict, List, Optional, Type, Any, Callable

from src.services.agents.interfaces import AgentInterface
from src.utils.logging import get_logger

logger = get_logger(__name__)

class AgentRegistry:
    """
    Registro de agentes disponíveis no sistema.
    Implementa o padrão Singleton para garantir um único registro global.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance._agents = {}
            cls._instance._agent_factories = {}
            logger.info("Registro de agentes inicializado")
        return cls._instance
    
    def register_agent_class(self, agent_type: str, agent_class: Type[AgentInterface]) -> None:
        """
        Registra uma classe de agente.
        
        Args:
            agent_type (str): Tipo do agente
            agent_class (Type[AgentInterface]): Classe do agente
        """
        if agent_type in self._agents:
            logger.warning(f"Substituindo classe de agente para o tipo '{agent_type}'")
        
        self._agents[agent_type] = agent_class
        logger.info(f"Classe de agente '{agent_class.__name__}' registrada para o tipo '{agent_type}'")
    
    def register_agent_factory(self, agent_type: str, factory: Callable[..., AgentInterface]) -> None:
        """
        Registra uma fábrica de agentes.
        
        Args:
            agent_type (str): Tipo do agente
            factory (Callable[..., AgentInterface]): Função de fábrica que cria instâncias do agente
        """
        if agent_type in self._agent_factories:
            logger.warning(f"Substituindo fábrica de agente para o tipo '{agent_type}'")
        
        self._agent_factories[agent_type] = factory
        logger.info(f"Fábrica de agente registrada para o tipo '{agent_type}'")
    
    def get_agent_class(self, agent_type: str) -> Optional[Type[AgentInterface]]:
        """
        Obtém a classe de um agente pelo tipo.
        
        Args:
            agent_type (str): Tipo do agente
            
        Returns:
            Optional[Type[AgentInterface]]: Classe do agente ou None se não encontrado
        """
        return self._agents.get(agent_type)
    
    def get_agent_factory(self, agent_type: str) -> Optional[Callable[..., AgentInterface]]:
        """
        Obtém a fábrica de um agente pelo tipo.
        
        Args:
            agent_type (str): Tipo do agente
            
        Returns:
            Optional[Callable[..., AgentInterface]]: Fábrica do agente ou None se não encontrada
        """
        return self._agent_factories.get(agent_type)
    
    def create_agent(self, agent_type: str, **kwargs) -> Optional[AgentInterface]:
        """
        Cria uma instância de um agente pelo tipo.
        
        Args:
            agent_type (str): Tipo do agente
            **kwargs: Argumentos para a criação do agente
            
        Returns:
            Optional[AgentInterface]: Instância do agente ou None se não for possível criar
        """
        # Tenta usar a fábrica registrada
        factory = self.get_agent_factory(agent_type)
        if factory:
            try:
                return factory(**kwargs)
            except Exception as e:
                logger.error(f"Erro ao criar agente do tipo '{agent_type}' usando fábrica: {str(e)}")
                return None
        
        # Se não houver fábrica, tenta usar a classe registrada
        agent_class = self.get_agent_class(agent_type)
        if agent_class:
            try:
                return agent_class(**kwargs)
            except Exception as e:
                logger.error(f"Erro ao criar agente do tipo '{agent_type}' usando classe: {str(e)}")
                return None
        
        logger.error(f"Nenhum agente do tipo '{agent_type}' registrado")
        return None
    
    def list_registered_agent_types(self) -> List[str]:
        """
        Lista todos os tipos de agentes registrados.
        
        Returns:
            List[str]: Lista de tipos de agentes
        """
        # Combina os tipos de agentes das classes e fábricas
        return list(set(list(self._agents.keys()) + list(self._agent_factories.keys())))

class AgentFactory:
    """
    Fábrica para criar instâncias de agentes.
    Utiliza o registro de agentes para criar as instâncias.
    """
    
    @staticmethod
    def create_agent(agent_type: str, **kwargs) -> Optional[AgentInterface]:
        """
        Cria uma instância de um agente pelo tipo.
        
        Args:
            agent_type (str): Tipo do agente
            **kwargs: Argumentos para a criação do agente
            
        Returns:
            Optional[AgentInterface]: Instância do agente ou None se não for possível criar
        """
        registry = AgentRegistry()
        return registry.create_agent(agent_type, **kwargs)
    
    @staticmethod
    def list_available_agent_types() -> List[str]:
        """
        Lista todos os tipos de agentes disponíveis.
        
        Returns:
            List[str]: Lista de tipos de agentes
        """
        registry = AgentRegistry()
        return registry.list_registered_agent_types()
