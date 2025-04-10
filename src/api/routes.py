"""
Rotas da API Flask.
"""
from flask import Blueprint, jsonify, render_template, request

from src.config.settings import active_config
from src.services.agent_orchestrator import AgentOrchestrator
from src.utils.statistics import prepare_chart_data
from src.utils.logging import get_logger

logger = get_logger(__name__)

# Cria um blueprint para as rotas
api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def index():
    """
    Rota principal que renderiza o template index.html.

    Returns:
        str: Template HTML renderizado
    """
    return render_template('index.html', loading=True)

@api_bp.route('/components/<component_name>')
def get_component(component_name):
    """
    Rota para obter componentes HTML.

    Args:
        component_name (str): Nome do componente a ser renderizado

    Returns:
        str: Template do componente renderizado
    """
    return render_template(f'components/{component_name}.html')

@api_bp.route('/fetch-data')
def fetch_data():
    """
    Rota para buscar dados de produtos da Amazon.

    Returns:
        Response: Resposta JSON com os produtos e dados para gráficos
    """
    try:
        # Obtém parâmetros opcionais da requisição
        fetcher_type = request.args.get('fetcher')
        processor_type = request.args.get('processor')
        source = request.args.get('source', active_config.DEFAULT_SCRAPE_URL)

        # Inicializa o orquestrador de agentes
        orchestrator = AgentOrchestrator()

        # Busca e processa os produtos
        produtos = orchestrator.fetch_and_process_products(
            source=source,
            fetcher_type=fetcher_type,
            processor_type=processor_type
        )

        if not produtos:
            logger.error("Erro ao obter ou processar dados")
            return jsonify({
                "success": False,
                "error": "Erro ao obter ou processar dados"
            })

        # Verifica se os produtos já estão no formato do agente
        if isinstance(produtos, list) and len(produtos) > 0 and isinstance(produtos[0], dict):
            # Já está no formato de dicionário (provavelmente do agente)
            logger.info("Produtos já estão no formato de dicionário")
            produtos_dict = produtos
        else:
            # Converte para dicionários para serialização JSON
            logger.info("Convertendo produtos para o formato de dicionário")
            produtos_dict = []
            for produto in produtos:
                # Garante que todos os campos necessários estão presentes
                produto_dict = {
                    "name": produto.name,
                    "price": float(produto.price) if produto.price is not None else 0.0,
                    "rating": float(produto.rating) if produto.rating is not None else 0.0,
                    "image_url": produto.image_url or "",
                    "url": produto.url or "",
                    "description": produto.description or ""
                }
                produtos_dict.append(produto_dict)

        # Prepara os dados para o gráfico
        dados_grafico = prepare_chart_data(produtos)

        # Registra os dados para debug
        logger.info(f"Produtos processados: {len(produtos_dict)}")
        logger.info(f"Dados do gráfico: {dados_grafico}")

        # Retorna os dados processados
        return jsonify({
            "success": True,
            "produtos": produtos_dict,
            "dados_grafico": dados_grafico
        })

    except Exception as e:
        logger.error(f"Erro no servidor: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Erro no servidor: {str(e)}"
        })

@api_bp.route('/agents')
def list_agents():
    """
    Rota para listar os agentes disponíveis.

    Returns:
        Response: Resposta JSON com os agentes disponíveis
    """
    try:
        orchestrator = AgentOrchestrator()
        agents = orchestrator.list_available_agents()

        return jsonify({
            "success": True,
            "agents": agents
        })

    except Exception as e:
        logger.error(f"Erro ao listar agentes: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Erro ao listar agentes: {str(e)}"
        })
