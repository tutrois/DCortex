"""
Configuração e inicialização de agentes.
"""
from typing import Dict, Any, List

from src.config.settings import active_config
from src.services.agents.registry import AgentRegistry
from src.services.agents.langflow import LangflowFetcherAgent, LangflowProcessorAgent
from src.utils.logging import get_logger

logger = get_logger(__name__)

def register_default_agents() -> None:
    """
    Registra os agentes padrão no registro de agentes.
    """
    registry = AgentRegistry()

    # Registra os agentes Langflow
    registry.register_agent_class("langflow_fetcher", LangflowFetcherAgent)
    registry.register_agent_class("langflow_processor", LangflowProcessorAgent)

    # Registra fábricas para criar agentes com configurações específicas
    registry.register_agent_factory(
        "coletor_dados_amazon_fetcher",
        lambda: LangflowFetcherAgent(
            api_url=active_config.LANGFLOW_API_URL,
            name="ColetorDadosAmazon - Busca",
            description="Agente especializado em buscar dados de produtos da Amazon"
        )
    )

    registry.register_agent_factory(
        "coletor_dados_amazon_processor",
        lambda: LangflowProcessorAgent(
            name="ColetorDadosAmazon - Processamento",
            description="Agente especializado em processar dados de produtos da Amazon"
        )
    )

    logger.info(f"Agentes padrão registrados: {registry.list_registered_agent_types()}")

def get_agent_config() -> Dict[str, Any]:
    """
    Retorna a configuração de agentes.

    Returns:
        Dict[str, Any]: Configuração de agentes
    """
    return {
        "default_fetcher": "coletor_dados_amazon_fetcher",
        "default_processor": "coletor_dados_amazon_processor",
        "available_agents": {
            "fetchers": [
                {
                    "id": "coletor_dados_amazon_fetcher",
                    "name": "ColetorDadosAmazon - Busca",
                    "description": "Agente especializado em buscar dados de produtos da Amazon"
                },
                {
                    "id": "langflow_fetcher",
                    "name": "Langflow Fetcher",
                    "description": "Agente genérico para busca de dados usando Langflow"
                }
            ],
            "processors": [
                {
                    "id": "coletor_dados_amazon_processor",
                    "name": "ColetorDadosAmazon - Processamento",
                    "description": "Agente especializado em processar dados de produtos da Amazon"
                },
                {
                    "id": "langflow_processor",
                    "name": "Langflow Processor",
                    "description": "Agente genérico para processamento de dados do Langflow"
                }
            ]
        }
    }

def get_available_agents() -> List[Dict[str, Any]]:
    """
    Retorna a lista de agentes disponíveis.

    Returns:
        List[Dict[str, Any]]: Lista de agentes disponíveis
    """
    registry = AgentRegistry()
    agent_types = registry.list_registered_agent_types()

    agents = []
    for agent_type in agent_types:
        # Cria uma instância temporária para obter metadados
        agent = registry.create_agent(agent_type)
        if agent:
            agents.append({
                "id": agent_type,
                "name": agent.agent_name,
                "type": agent.agent_type,
                "description": agent.description
            })

    return agents
