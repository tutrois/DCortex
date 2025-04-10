"""
Implementações de agentes Langflow.
"""
from src.services.agents.langflow.fetcher import LangflowFetcherAgent
from src.services.agents.langflow.processor import LangflowProcessorAgent

__all__ = [
    'LangflowFetcherAgent',
    'LangflowProcessorAgent'
]
