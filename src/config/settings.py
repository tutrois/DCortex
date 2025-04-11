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
    LANGFLOW_API_URL = os.getenv('LANGFLOW_API_URL', 'http://127.0.0.1:7860/api/v1/run/98bc1dc9-3bb8-4941-ad26-3e26e775c31b')
    
    # Configurações de API
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Configurações de timeout e retry
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 500))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 5))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 10))
    
    # URL padrão para scraping
    DEFAULT_SCRAPE_URL = os.getenv(
        'DEFAULT_SCRAPE_URL', 
        'https://www.amazon.com.br/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0'
    )

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
