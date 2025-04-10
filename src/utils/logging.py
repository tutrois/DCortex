"""
Configuração de logging para a aplicação.
"""
import logging
import sys
from typing import Optional

def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Configura e retorna um logger.
    
    Args:
        name (str): Nome do logger
        level (Optional[int]): Nível de logging. Se None, usa INFO.
        
    Returns:
        logging.Logger: Logger configurado
    """
    if level is None:
        level = logging.INFO
        
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicação de handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
