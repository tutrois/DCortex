"""
Agente para formatação de dados do Langflow.
"""
import json
import time
import requests
from typing import List, Dict, Any, Union, Optional

from src.services.agents.base import BaseDataProcessorAgent
from src.utils.logging import get_logger
from src.config.settings import active_config

logger = get_logger(__name__)

class LangflowFormatterAgent(BaseDataProcessorAgent):
    """
    Agente para formatação de dados processados pelo Langflow.
    """

    def __init__(self, name: str = "Langflow Formatter",
                 description: str = "Agente para formatação de dados processados pelo Langflow",
                 api_url: str = None,
                 timeout: int = None,
                 max_retries: int = None):
        """
        Inicializa o agente de formatação Langflow.

        Args:
            name (str): Nome do agente
            description (str): Descrição do agente
            api_url (str): URL da API do Langflow (opcional)
            timeout (int): Timeout para requisições em segundos (opcional)
            max_retries (int): Número máximo de tentativas (opcional)
        """
        super().__init__(name, description)
        self.url = api_url or active_config.LANGFLOW_FORMATTER_API_URL
        self.timeout = timeout or active_config.REQUEST_TIMEOUT
        self.max_retries = max_retries or active_config.MAX_RETRIES

    def process_data(self, data: Union[str, List[Dict[str, Any]]]) -> Union[List[Dict[str, Any]], None]:
        """
        Formata os dados processados pelo agente anterior usando a API do Langflow.

        Args:
            data (Union[str, List[Dict[str, Any]]]): Dados processados pelo agente anterior
                Pode ser uma string JSON ou uma lista de dicionários

        Returns:
            Union[List[Dict[str, Any]], None]: Lista de produtos formatados ou None em caso de erro
        """
        if not data:
            logger.error("Dados vazios recebidos para formatação")
            return None

        try:
            # Converte os dados para o formato esperado pelo Langflow
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                logger.info("Recebeu lista de dicionários, convertendo para JSON")
                input_data = json.dumps(data)
            elif isinstance(data, str):
                # Verifica explicitamente se é uma string
                logger.info(f"Recebeu dado do tipo: {type(data).__name__}")

                # Verifica se a string não está vazia
                if not data.strip():
                    logger.error("String recebida está vazia ou contém apenas espaços")
                    return None

                # Verifica se é um JSON válido
                try:
                    # Tenta validar como JSON
                    json.loads(data)
                    logger.info("Recebeu string JSON válida")
                    input_data = data
                except json.JSONDecodeError as e:
                    # Se não for um JSON válido, pode ser apenas texto bruto
                    logger.info("Recebeu texto bruto (não é JSON)")
                    logger.debug(f"Primeiros 200 caracteres do texto: {data[:200]}")
                    # Usa o texto como está, sem tentar interpretá-lo como JSON
                    input_data = data
            else:
                logger.error(f"Formato de dados não suportado: {type(data)}")
                return None

            # Prepara o payload para a API do Langflow
            payload = self._prepare_payload(input_data)
            headers = self._get_headers()

            # Faz a requisição para a API do Langflow
            response_text = self._make_request(payload, headers)
            if not response_text:
                logger.error("Não foi possível obter resposta da API do Langflow")
                return None

            # Log detalhado da resposta
            logger.info("Resposta recebida do Langflow")
            logger.debug(f"Primeiros 1000 caracteres da resposta: {response_text[:1000]}")

            # Processa a resposta
            try:
                response_data = json.loads(response_text)
                logger.info("Resposta convertida para JSON com sucesso")
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao converter resposta para JSON: {e}")
                logger.error(f"Resposta inválida: {response_text[:500]}...")
                return None

            # Tenta extrair os produtos
            formatted_products = self._extract_products_from_response(response_data)

            # Log do resultado da extração
            if formatted_products:
                logger.info(f"Produtos extraídos com sucesso: {len(formatted_products)} produtos")
                logger.debug(f"Primeiro produto: {json.dumps(formatted_products[0]) if formatted_products else 'Nenhum'}")
            else:
                logger.error("Não foi possível extrair produtos da resposta")

            if not formatted_products:
                logger.error("Não foi possível extrair produtos formatados da resposta")
                return None

            return formatted_products
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao formatar dados: {str(e)}")
            return None

    def _prepare_payload(self, input_data: str) -> Dict[str, Any]:
        """
        Prepara o payload para a API do Langflow.

        Args:
            input_data (str): Dados de entrada em formato JSON ou texto bruto

        Returns:
            Dict[str, Any]: Payload para a API
        """
        # Verifica se input_data é uma string
        if not isinstance(input_data, str):
            logger.warning(f"input_data não é uma string, é do tipo: {type(input_data).__name__}")
            try:
                # Tenta converter para string
                input_data = str(input_data)
                logger.info("Converteu input_data para string")
            except Exception as e:
                logger.error(f"Erro ao converter input_data para string: {str(e)}")
                # Usa uma string vazia como fallback
                input_data = ""

        return {
            "inputs": {
                "text": input_data
            }
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

                response.raise_for_status()

                # Verifica se a resposta é um JSON válido
                try:
                    data = response.json()
                    logger.info("Resposta JSON recebida com sucesso")
                    logger.info(f"Estrutura da resposta: {json.dumps(data)[:200]}...")

                    # Log adicional para depuração
                    response_text = response.text
                    logger.info(f"Resposta completa do Langflow (primeiros 500 caracteres): {response_text[:500]}...")

                    return response_text
                except json.JSONDecodeError:
                    logger.error("Resposta não é um JSON válido")
                    logger.error(f"Conteúdo da resposta: {response.text[:500]}")  # Mostra os primeiros 500 caracteres
                    return None

            except requests.exceptions.RequestException as e:
                logger.error(f"Erro na requisição (tentativa {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:  # Última tentativa
                    logger.error("Número máximo de tentativas atingido")
                    return None
                time.sleep(active_config.RETRY_DELAY)  # Espera antes de tentar novamente

        return None

    def _extract_products_from_response(self, response_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        Extrai a lista de produtos formatados da estrutura de resposta aninhada do Langflow.

        Args:
            response_data (Dict[str, Any]): Dados da resposta do Langflow

        Returns:
            Optional[List[Dict[str, Any]]]: Lista de produtos formatados ou None se não for possível extrair
        """
        try:
            # Log da estrutura da resposta para depuração
            logger.info(f"Estrutura da resposta: {json.dumps(response_data)[:500]}...")

            # Tenta extrair produtos de diferentes maneiras

            # Método 0: Estrutura específica para o formato {"results": {"text": {"text_key": "text", "data": {"text": "[...]"}}}}
            if "outputs" in response_data and len(response_data["outputs"]) > 0:
                outputs = response_data["outputs"][0]
                logger.info(f"Outputs encontrados: {json.dumps(outputs)[:200]}...")

                if "outputs" in outputs and len(outputs["outputs"]) > 0:
                    outputssecond = outputs["outputs"][0]
                    logger.info(f"Segundo nível de outputs: {json.dumps(outputssecond)[:200]}")

                    # Verifica se tem a estrutura esperada com "results" > "text" > "data" > "text"
                    if isinstance(outputssecond, dict) and "results" in outputssecond:
                        results_obj = outputssecond["results"]
                        logger.info(f"Objeto results: {json.dumps(results_obj)[:200]}")

                        if isinstance(results_obj, dict) and "text" in results_obj:
                            text_obj = results_obj["text"]
                            logger.info(f"Objeto text: {json.dumps(text_obj)[:200]}")

                            if isinstance(text_obj, dict) and "data" in text_obj:
                                data_obj = text_obj["data"]
                                logger.info(f"Objeto data: {json.dumps(data_obj)[:200]}")

                                if isinstance(data_obj, dict) and "text" in data_obj:
                                    text_content = data_obj["text"]
                                    logger.info(f"Conteúdo text: {text_content[:200]}")

                                    # Tenta converter o conteúdo para JSON
                                    try:
                                        products = json.loads(text_content)
                                        if isinstance(products, list):
                                            logger.info(f"Extraiu {len(products)} produtos do campo 'text' em 'data' (Método 0)")
                                            return products
                                        else:
                                            logger.warning(f"O conteúdo de 'text' não é uma lista: {type(products)}")
                                    except json.JSONDecodeError as e:
                                        logger.warning(f"Não foi possível decodificar o JSON do campo 'text': {e}")

            # Método 1: Estrutura padrão do Langflow
            if "outputs" in response_data and len(response_data["outputs"]) > 0:
                outputs = response_data["outputs"][0]
                logger.info(f"Outputs encontrados: {json.dumps(outputs)[:200]}...")

                if "outputs" in outputs and len(outputs["outputs"]) > 0:
                    outputssecond = outputs["outputs"][0]
                    logger.info(f"Tipo do resultado: {json.dumps(outputssecond)[:200]}")

                if "data" in outputssecond and len(outputssecond["data"]) > 0:
                    results = outputssecond["data"][0]
                    logger.info(f"Tipo do resultado: {json.dumps(results)[:200]}")

                    # Verifica se o resultado é uma string JSON
                    if isinstance(results, str):
                        logger.info(f"Resultado é uma string. Primeiros 200 caracteres: {results[:200]}...")
                        try:
                            products = json.loads(results)
                            logger.info(f"Tipo após parse JSON: {type(products)}")

                            if isinstance(products, list):
                                logger.info(f"Extraiu {len(products)} produtos formatados (Método 1)")
                                return products
                            elif isinstance(products, dict) and "data" in products:
                                # Tenta extrair do campo "data"
                                data_content = products.get("data")
                                if isinstance(data_content, list):
                                    logger.info(f"Extraiu {len(data_content)} produtos do campo 'data' (Método 1.1)")
                                    return data_content
                            else:
                                logger.warning(f"Resultado não é uma lista após parse JSON: {type(products)}")
                        except json.JSONDecodeError as e:
                            logger.warning(f"Não foi possível decodificar o JSON da resposta: {e}")
                    # Verifica se o resultado já é uma lista
                    elif isinstance(results, list):
                        logger.info(f"Resultado já é uma lista com {len(results)} itens (Método 1.2)")
                        return results
                    # Verifica se o resultado é um dicionário
                    elif isinstance(results, dict):
                        # Tenta extrair do campo "data"
                        if "data" in results:
                            data_content = results.get("data")
                            if isinstance(data_content, list):
                                logger.info(f"Extraiu {len(data_content)} produtos do campo 'data' (Método 1.3)")
                                return data_content
                        # Tenta extrair do campo "products"
                        elif "products" in results:
                            products_content = results.get("products")
                            if isinstance(products_content, list):
                                logger.info(f"Extraiu {len(products_content)} produtos do campo 'products' (Método 1.4)")
                                return products_content

                if isinstance(value, list) and len(value) > 0 and all(isinstance(item, dict) for item in value):
                    logger.info(f"Encontrou lista de dicionários no campo '{key}' (Método 3)")
                    return value
                elif isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, list) and len(subvalue) > 0 and all(isinstance(item, dict) for item in subvalue):
                            logger.info(f"Encontrou lista de dicionários no campo '{key}.{subkey}' (Método 3.1)")
                            return subvalue

            logger.error("Não foi possível extrair produtos da resposta usando nenhum método")
            logger.error(f"Estrutura de resposta completa: {json.dumps(response_data)}")
            return None
        except Exception as e:
            logger.error(f"Erro ao extrair produtos da resposta: {str(e)}")
            return None
