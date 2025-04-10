"""
Testes para o processador de dados.
"""
import json
import pytest
from src.services.data_processor import LangflowDataProcessor

def test_process_data_success():
    """Testa o processamento de dados com sucesso."""
    # Cria uma resposta simulada do Langflow
    mock_response = {
        "outputs": [
            {
                "outputs": [
                    {
                        "results": {
                            "text": {
                                "data": {
                                    "text": json.dumps([
                                        {
                                            "nome": "Produto 1",
                                            "preço": 99.99,
                                            "avaliação": 4.5
                                        },
                                        {
                                            "nome": "Produto 2",
                                            "preço": 199.99,
                                            "avaliação": 3.5
                                        }
                                    ])
                                }
                            }
                        }
                    }
                ]
            }
        ]
    }
    
    processor = LangflowDataProcessor()
    result = processor.process_data(json.dumps(mock_response))
    
    assert result is not None
    assert len(result) == 2
    assert result[0]["nome"] == "Produto 1"
    assert result[0]["preço"] == 99.99
    assert result[1]["nome"] == "Produto 2"
    assert result[1]["preço"] == 199.99

def test_process_data_invalid_json():
    """Testa o processamento com JSON inválido."""
    processor = LangflowDataProcessor()
    result = processor.process_data("invalid json")
    
    assert result is None

def test_process_data_empty():
    """Testa o processamento com dados vazios."""
    processor = LangflowDataProcessor()
    result = processor.process_data("")
    
    assert result is None

def test_process_data_invalid_structure():
    """Testa o processamento com estrutura inválida."""
    # Cria uma resposta com estrutura diferente da esperada
    mock_response = {
        "different_key": "value"
    }
    
    processor = LangflowDataProcessor()
    result = processor.process_data(json.dumps(mock_response))
    
    assert result is None
