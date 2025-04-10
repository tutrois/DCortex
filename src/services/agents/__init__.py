"""
Pacote de agentes para processamento de dados.
"""
from src.services.agents.interfaces import AgentInterface, DataFetcherAgentInterface, DataProcessorAgentInterface
from src.services.agents.base import BaseAgent, BaseDataFetcherAgent, BaseDataProcessorAgent
from src.services.agents.registry import AgentRegistry, AgentFactory

__all__ = [
    'AgentInterface',
    'DataFetcherAgentInterface',
    'DataProcessorAgentInterface',
    'BaseAgent',
    'BaseDataFetcherAgent',
    'BaseDataProcessorAgent',
    'AgentRegistry',
    'AgentFactory'
]
