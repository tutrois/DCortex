"""
Agente para busca de dados usando Langflow.
"""
import json
import time
import requests
from typing import Optional, Dict, Any

from src.config.settings import active_config
from src.services.agents.base import BaseDataFetcherAgent
from src.utils.logging import get_logger

logger = get_logger(__name__)

class LangflowFetcherAgent(BaseDataFetcherAgent):
    """
    Agente para busca de dados usando a API do Langflow.
    """
    
    def __init__(self, api_url: Optional[str] = None, name: str = "Langflow Fetcher", 
                 description: str = "Agente para busca de dados usando a API do Langflow"):
        """
        Inicializa o agente Langflow.
        
        Args:
            api_url (Optional[str]): URL da API do Langflow. Se None, usa a configuração padrão.
            name (str): Nome do agente
            description (str): Descrição do agente
        """
        super().__init__(name, description)
        self.url = api_url or active_config.LANGFLOW_API_URL
        self.max_retries = active_config.MAX_RETRIES
        self.retry_delay = active_config.RETRY_DELAY
        self.timeout = active_config.REQUEST_TIMEOUT
        
    def fetch_data(self, source: str) -> Optional[str]:
        """
        Busca dados usando o Langflow.
        
        Args:
            source (str): URL ou texto a ser processado pelo Langflow
            
        Returns:
            Optional[str]: Resposta do Langflow ou None em caso de erro
        """
        # Remove o prefixo r.jina.ai se presente
        if "r.jina.ai/" in source:
            source = source.split("https://r.jina.ai/")[1]
            
        payload = self._prepare_payload(source)
        headers = self._get_headers()
        
        return self._make_request(payload, headers)
    
    def _prepare_payload(self, input_value: str) -> Dict[str, Any]:
        """
        Prepara o payload para a requisição.
        
        Args:
            input_value (str): Valor de entrada para o Langflow
            
        Returns:
            Dict[str, Any]: Payload formatado
        """
        return {
            "input_value": input_value,
            "output_type": "text",
            "input_type": "text"
        }
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Obtém os cabeçalhos para a requisição.
        
        Returns:
            Dict[str, str]: Cabeçalhos HTTP
        """
        return {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def _make_request(self, payload: Dict[str, Any], headers: Dict[str, str]) -> Optional[str]:
        """
        Faz a requisição para a API do Langflow com retry.
        
        Args:
            payload (Dict[str, Any]): Payload da requisição
            headers (Dict[str, str]): Cabeçalhos da requisição
            
        Returns:
            Optional[str]: Resposta da API ou None em caso de erro
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Tentativa {attempt + 1} de {self.max_retries}")
                logger.info(f"Fazendo requisição para URL: {self.url}")
                
                response = requests.request(
                    "POST", 
                    self.url, 
                    json=payload, 
                    headers=headers,
                    timeout=self.timeout
                )
                
                logger.info(f"Status Code: {response.status_code}")
                
                if response.status_code == 504:
                    logger.warning("Erro 504 (Gateway Timeout) detectado. Tentando novamente...")
                    if attempt < self.max_retries - 1:
                        logger.info(f"Aguardando {self.retry_delay} segundos antes da próxima tentativa...")
                        time.sleep(self.retry_delay)
                        continue
                    else:
                        logger.error("Número máximo de tentativas atingido.")
                        return None
                
                response.raise_for_status()
                
                # Verifica se a resposta é um JSON válido
                try:
                    response_data = response.json()
                    logger.info("Resposta recebida com sucesso")
                    return response.text
                except json.JSONDecodeError:
                    logger.error("Resposta não é um JSON válido")
                    logger.error(f"Conteúdo da resposta: {response.text[:500]}")  # Mostra os primeiros 500 caracteres
                    return None
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout na tentativa {attempt + 1}. Tentando novamente...")
                if attempt < self.max_retries - 1:
                    logger.info(f"Aguardando {self.retry_delay} segundos antes da próxima tentativa...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Número máximo de tentativas atingido.")
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro na requisição à API: {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"Aguardando {self.retry_delay} segundos antes da próxima tentativa...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Número máximo de tentativas atingido.")
                    return None
                    
        return None
