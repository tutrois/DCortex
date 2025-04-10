"""
Aplicação principal Flask.
"""
from flask import Flask
import os

from src.api.routes import api_bp
from src.config.settings import config_by_name
from src.config.agents import register_default_agents
from src.utils.logging import get_logger

logger = get_logger(__name__)

def create_app(config_name='development'):
    """
    Factory para criar a aplicação Flask.

    Args:
        config_name (str): Nome da configuração a ser usada

    Returns:
        Flask: Aplicação Flask configurada
    """
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # Carrega configurações
    app.config.from_object(config_by_name[config_name])

    # Registra agentes padrão
    register_default_agents()
    logger.info("Agentes padrão registrados")

    # Registra blueprints
    app.register_blueprint(api_bp)

    logger.info(f"Aplicação iniciada no ambiente: {config_name}")

    return app

def run_app():
    """
    Função para executar a aplicação.
    """
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    debug = env != 'production'
    app.run(debug=debug)

if __name__ == '__main__':
    run_app()
