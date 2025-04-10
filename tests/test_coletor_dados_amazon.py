"""
Testes para o agente ColetorDadosAmazon.
"""
import pytest
from unittest.mock import patch, MagicMock

from src.services.agents.registry import AgentRegistry
from src.config.agents import register_default_agents

def test_coletor_dados_amazon_registro():
    """Testa se o agente ColetorDadosAmazon está registrado corretamente."""
    # Registra os agentes padrão
    register_default_agents()
    
    # Obtém o registro de agentes
    registry = AgentRegistry()
    
    # Verifica se os agentes do ColetorDadosAmazon estão registrados
    assert "coletor_dados_amazon_fetcher" in registry.list_registered_agent_types()
    assert "coletor_dados_amazon_processor" in registry.list_registered_agent_types()

def test_coletor_dados_amazon_criacao():
    """Testa a criação de instâncias do agente ColetorDadosAmazon."""
    # Registra os agentes padrão
    register_default_agents()
    
    # Obtém o registro de agentes
    registry = AgentRegistry()
    
    # Cria instâncias dos agentes
    fetcher = registry.create_agent("coletor_dados_amazon_fetcher")
    processor = registry.create_agent("coletor_dados_amazon_processor")
    
    # Verifica se as instâncias foram criadas corretamente
    assert fetcher is not None
    assert processor is not None
    
    # Verifica os nomes dos agentes
    assert fetcher.agent_name == "ColetorDadosAmazon - Busca"
    assert processor.agent_name == "ColetorDadosAmazon - Processamento"

@patch('src.services.agents.langflow.fetcher.requests.request')
def test_coletor_dados_amazon_fetch(mock_request):
    """Testa a funcionalidade de busca do agente ColetorDadosAmazon."""
    # Configura o mock para simular uma resposta bem-sucedida
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"outputs": [{"outputs": [{"results": {"text": {"data": {"text": "[]"}}}}]}]}'
    mock_response.json.return_value = {"outputs": [{"outputs": [{"results": {"text": {"data": {"text": "[]"}}}}]}]}
    mock_request.return_value = mock_response
    
    # Registra os agentes padrão
    register_default_agents()
    
    # Obtém o registro de agentes
    registry = AgentRegistry()
    
    # Cria uma instância do agente de busca
    fetcher = registry.create_agent("coletor_dados_amazon_fetcher")
    
    # Testa a funcionalidade de busca
    result = fetcher.fetch_data("https://example.com")
    
    # Verifica se o resultado é o esperado
    assert result == '{"outputs": [{"outputs": [{"results": {"text": {"data": {"text": "[]"}}}}]}]}'
    
    # Verifica se o método request foi chamado com os parâmetros corretos
    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert kwargs["method"] == "POST"
    assert "json" in kwargs
    assert kwargs["json"]["input_value"] == "https://example.com"
