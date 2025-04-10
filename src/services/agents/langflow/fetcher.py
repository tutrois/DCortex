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
        # Log para depuração
        logger.info(f"Fetcher recebeu URL original: {source}")

        # Garante que a URL seja válida
        if not source or not isinstance(source, str):
            logger.error(f"URL inválida: {source}")
            return None

        # Formata a URL para o formato esperado pelo bot
        formatted_url = self._format_url_for_bot(source)
        logger.info(f"URL formatada para o bot: {formatted_url}")

        # Prepara o payload com a URL formatada
        payload = self._prepare_payload(formatted_url)
        headers = self._get_headers()

        return self._make_request(payload, headers)

    def _format_url_for_bot(self, url: str) -> str:
        """
        Formata a URL para o formato esperado pelo bot.
        O bot espera receber a URL com o prefixo r.jina.ai.

        Args:
            url (str): URL original

        Returns:
            str: URL formatada com o prefixo r.jina.ai
        """
        # Log da URL original
        logger.info(f"Formatando URL para o bot. URL original: {url}")

        # Primeiro, remove o prefixo r.jina.ai se já estiver presente
        # para evitar prefixos duplicados
        if "r.jina.ai/" in url:
            try:
                # Extrai a URL original após o prefixo r.jina.ai
                url = url.split("https://r.jina.ai/")[1]
                logger.info(f"Prefixo r.jina.ai removido, URL base: {url}")
            except IndexError:
                # Se falhar, tenta outro formato
                parts = url.split("r.jina.ai/")
                if len(parts) > 1:
                    url = parts[1]
                    logger.info(f"Prefixo r.jina.ai removido (formato alternativo), URL base: {url}")

        # Garante que a URL tenha um protocolo (http:// ou https://)
        if not url.startswith("http"):
            url = f"https://{url}"
            logger.info(f"Adicionado protocolo https:// à URL: {url}")

        # Adiciona o prefixo r.jina.ai à URL limpa
        formatted_url = f"https://r.jina.ai/{url}"
        logger.info(f"URL formatada com prefixo r.jina.ai: {formatted_url}")

        # Garante que a URL esteja no formato correto para o Langflow
        # Verifica se a URL tem dois https:// (pode acontecer em algumas manipulações)
        if "https://https://" in formatted_url:
            formatted_url = formatted_url.replace("https://https://", "https://")
            logger.warning(f"URL corrigida para remover https:// duplicado: {formatted_url}")

        # Verifica se a URL tem o formato correto
        if not formatted_url.startswith("https://r.jina.ai/http"):
            logger.error(f"URL mal formatada: {formatted_url}")
            logger.error("A URL deve ter o formato https://r.jina.ai/https://...")

        # Log da URL final
        logger.info(f"URL final formatada: {formatted_url}")

        return formatted_url

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
        # Log do payload para depuração
        logger.info(f"Payload da requisição: {json.dumps(payload)}")

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Tentativa {attempt + 1} de {self.max_retries}")
                logger.info(f"Fazendo requisição para URL: {self.url}")

                # Adiciona headers para evitar cache
                headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                headers['Pragma'] = 'no-cache'
                headers['Expires'] = '0'

                # Adiciona um timestamp ao payload para evitar cache
                payload['timestamp'] = str(time.time())

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
                    data = response.json()
                    logger.info("Resposta JSON recebida com sucesso")
                    logger.info(f"Estrutura da resposta: {json.dumps(data)[:200]}...")

                    # Verifica se a resposta contém o prefixo r.jina.ai
                    response_text = response.text
                    if "r.jina.ai" in response_text:
                        logger.warning(f"A resposta contém o prefixo r.jina.ai: {response_text[:200]}...")

                    # Log adicional para depuração
                    logger.info(f"Resposta completa do Langflow (primeiros 500 caracteres): {response_text[:500]}...")

                    return response_text
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
