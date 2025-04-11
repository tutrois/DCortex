"""
Agente para processamento de dados do Langflow.
"""
import json
from typing import List, Dict, Any, Union, Optional

from src.services.agents.base import BaseDataProcessorAgent
from src.utils.logging import get_logger

logger = get_logger(__name__)

class LangflowProcessorAgent(BaseDataProcessorAgent):
    """
    Agente para processamento de dados retornados pelo Langflow.
    """
    
    def __init__(self, name: str = "Langflow Processor", 
                 description: str = "Agente para processamento de dados retornados pelo Langflow"):
        """
        Inicializa o agente de processamento Langflow.
        
        Args:
            name (str): Nome do agente
            description (str): Descrição do agente
        """
        super().__init__(name, description)
    
    def process_data(self, data: str) -> Union[List[Dict[str, Any]], None]:
        """
        Processa os dados JSON retornados pelo Langflow.
        
        Args:
            data (str): String JSON retornada pelo Langflow
            
        Returns:
            Union[List[Dict[str, Any]], None]: Lista de produtos processados ou None em caso de erro
        """
        if not data:
            logger.error("Dados vazios recebidos para processamento")
            return None
            
        try:
            # Converte a string JSON para um dicionário
            response_data = json.loads(data)
            
            # Navega pela estrutura aninhada para extrair os produtos
            products = self._extract_products_from_response(response_data)
            
            if not products:
                logger.error("Não foi possível extrair produtos da resposta")
                return None
                
            return products
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None
        except KeyError as e:
            logger.error(f"Chave não encontrada na estrutura de dados: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao processar dados: {e}")
            return None
    
    def _extract_products_from_response(self, response_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        Extrai a lista de produtos da estrutura de resposta aninhada do Langflow.
        
        Args:
            response_data (Dict[str, Any]): Dados da resposta do Langflow
            
        Returns:
            Optional[List[Dict[str, Any]]]: Lista de produtos ou None se não for possível extrair
        """
        try:
            # Verifica a estrutura da resposta
            if "outputs" in response_data and len(response_data["outputs"]) > 0:
                outputs = response_data["outputs"][0]
                if "outputs" in outputs and len(outputs["outputs"]) > 0:
                    results = outputs["outputs"][0]
                    if "results" in results and "text" in results["results"]:
                        text_data = results["results"]["text"]

                        # Agora sim, temos a lista de produtos
                        produtos = text_data["text"]
                        
                        return produtos
            
            logger.error("Estrutura da resposta não é a esperada")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao extrair produtos da resposta: {e}")
            return None
