"""
Serviço de orquestração de agentes.
Coordena a execução de múltiplos agentes para realizar tarefas complexas.
"""
from typing import Any, Dict, List, Optional, Union

from src.config.agents import get_agent_config
from src.config.settings import active_config
from src.models.product import Product
from src.services.agents.interfaces import DataFetcherAgentInterface, DataProcessorAgentInterface
from src.services.agents.registry import AgentFactory
from src.utils.logging import get_logger

logger = get_logger(__name__)

class AgentOrchestrator:
    """
    Orquestrador de agentes.
    Coordena a execução de múltiplos agentes para realizar tarefas complexas.
    """

    def __init__(self):
        """
        Inicializa o orquestrador de agentes.
        """
        self.agent_config = get_agent_config()
        self.factory = AgentFactory()
        logger.info("Orquestrador de agentes inicializado")

    def fetch_and_process_data(self, source: str,
                               fetcher_type: Optional[str] = None,
                               processor_type: Optional[str] = None,
                               formatter_type: Optional[str] = None) -> Union[List[Dict[str, Any]], None]:
        """
        Busca e processa dados usando os agentes especificados.

        Args:
            source (str): Fonte dos dados
            fetcher_type (Optional[str]): Tipo do agente de busca. Se None, usa o padrão.
            processor_type (Optional[str]): Tipo do agente de processamento. Se None, usa o padrão.
            formatter_type (Optional[str]): Tipo do agente de formatação. Se None, usa o padrão.

        Returns:
            Union[List[Dict[str, Any]], None]: Dados processados ou None em caso de erro
        """
        # Determina os tipos de agentes a serem usados
        fetcher_type = fetcher_type or self.agent_config["default_fetcher"]
        processor_type = processor_type or self.agent_config["default_processor"]
        formatter_type = formatter_type or self.agent_config.get("default_formatter")

        # Cria os agentes
        fetcher = self.factory.create_agent(fetcher_type)
        processor = self.factory.create_agent(processor_type)
        formatter = self.factory.create_agent(formatter_type) if formatter_type else None

        if not fetcher or not isinstance(fetcher, DataFetcherAgentInterface):
            logger.error(f"Agente de busca '{fetcher_type}' não encontrado ou inválido")
            return None

        if not processor or not isinstance(processor, DataProcessorAgentInterface):
            logger.error(f"Agente de processamento '{processor_type}' não encontrado ou inválido")
            return None

        if formatter_type and (not formatter or not isinstance(formatter, DataProcessorAgentInterface)):
            logger.error(f"Agente de formatação '{formatter_type}' não encontrado ou inválido")
            return None

        # Executa a busca
        raw_data = fetcher.fetch_data(source)
        if not raw_data:
            logger.error("Falha ao buscar dados")
            return None

        # Processa os dados
        processed_data = processor.process_data(raw_data)
        if not processed_data:
            logger.error("Falha ao processar dados")
            return None

        # Log do tipo de dados processados
        logger.info(f"Tipo de dados processados: {type(processed_data)}")

        # Extrai o conteúdo do campo "data" > "text" se for uma lista de dicionários
        if isinstance(processed_data, list) and len(processed_data) > 0:
            try:
                # Verifica se o primeiro item tem a estrutura esperada
                first_item = processed_data[0]
                if isinstance(first_item, dict) and "results" in first_item:
                    results = first_item.get("results", {})
                    if isinstance(results, dict) and "text" in results:
                        text_obj = results.get("text", {})
                        if isinstance(text_obj, dict) and "data" in text_obj:
                            data_obj = text_obj.get("data", {})
                            if isinstance(data_obj, dict) and "text" in data_obj:
                                # Extrai apenas o texto
                                text_content = data_obj.get("text", "")

                                # Verifica se o texto extraído é uma string
                                if isinstance(text_content, str):
                                    logger.info("Extraiu o conteúdo do campo 'data' > 'text' como string")
                                    logger.debug(f"Primeiros 200 caracteres do texto: {text_content[:200]}")
                                    processed_data = text_content
                                else:
                                    logger.warning(f"O conteúdo do campo 'data' > 'text' não é uma string, é do tipo: {type(text_content).__name__}")
                                    # Tenta converter para string se não for None
                                    if text_content is not None:
                                        try:
                                            processed_data = str(text_content)
                                            logger.info("Converteu o conteúdo para string")
                                        except Exception as e:
                                            logger.error(f"Erro ao converter para string: {str(e)}")
            except Exception as e:
                logger.error(f"Erro ao extrair conteúdo do campo 'data' > 'text': {str(e)}")
                # Continua com os dados originais

        if isinstance(processed_data, str):
            logger.info("Dados processados retornados como string")
        elif isinstance(processed_data, list):
            logger.info(f"Dados processados retornados como lista com {len(processed_data)} itens")

        # Formata os dados, se houver um formatador
        if formatter:
            logger.info("Formatando dados processados")
            formatted_data = formatter.process_data(processed_data)
            if not formatted_data:
                logger.error("Falha ao formatar dados")
                return None

            # Log do tipo de dados formatados
            logger.info(f"Tipo de dados formatados: {type(formatted_data)}")
            if isinstance(formatted_data, list):
                logger.info(f"Dados formatados retornados como lista com {len(formatted_data)} itens")

            return formatted_data

        return processed_data

    def fetch_and_process_products(self, source: str,
                                  fetcher_type: Optional[str] = None,
                                  processor_type: Optional[str] = None,
                                  formatter_type: Optional[str] = None) -> List[Product]:
        """
        Busca e processa produtos usando os agentes especificados.

        Args:
            source (str): Fonte dos dados
            fetcher_type (Optional[str]): Tipo do agente de busca. Se None, usa o padrão.
            processor_type (Optional[str]): Tipo do agente de processamento. Se None, usa o padrão.
            formatter_type (Optional[str]): Tipo do agente de formatação. Se None, usa o padrão.

        Returns:
            List[Product]: Lista de produtos processados
        """
        # Log para depuração
        logger.info(f"Orquestrador recebeu URL: {source}")

        # Verifica se a URL é válida
        if not source or not isinstance(source, str):
            logger.error(f"URL inválida recebida pelo orquestrador: {source}")
            source = active_config.DEFAULT_SCRAPE_URL
            logger.warning(f"Usando URL padrão: {source}")

        # Busca e processa os dados
        logger.info(f"Iniciando busca e processamento com URL: {source}")
        products_data = self.fetch_and_process_data(source, fetcher_type, processor_type, formatter_type)

        if not products_data:
            logger.error("Nenhum produto encontrado")
            return []

        # Converte para objetos Product
        products = [Product.from_dict(product) for product in products_data]
        logger.info(f"Processados {len(products)} produtos")

        return products

    def list_available_agents(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Lista os agentes disponíveis por tipo.

        Returns:
            Dict[str, List[Dict[str, Any]]]: Dicionário com agentes por tipo
        """
        return self.agent_config["available_agents"]
