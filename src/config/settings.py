"""
Módulo de configurações da aplicação.
Centraliza todas as configurações e variáveis de ambiente.
"""
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da aplicação
class Config:
    """Classe base de configuração."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta-padrao')

    # Configurações do Langflow
    LANGFLOW_FETCHER_API_URL = os.getenv('LANGFLOW_FETCHER_API_URL')
    LANGFLOW_FORMATTER_API_URL = os.getenv('LANGFLOW_FORMATTER_API_URL')

    # Configurações de API
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Configurações de timeout e retry
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY'))

    # URL padrão para scraping
    DEFAULT_SCRAPE_URL = os.getenv('DEFAULT_SCRAPE_URL')

class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento."""
    DEBUG = True

class TestingConfig(Config):
    """Configuração para ambiente de testes."""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Configuração para ambiente de produção."""
    # Configurações específicas para produção
    pass

# Mapeamento de configurações por ambiente
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Configuração ativa baseada na variável de ambiente ou padrão para desenvolvimento
active_config = config_by_name[os.getenv('FLASK_ENV', 'development')]
