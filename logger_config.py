"""
Logging configuration untuk chatbot
"""
import logging
import logging.handlers
import os
from config import LOG_LEVEL, LOG_FILE

def setup_logging():
    """Setup logging dengan file dan console handlers"""
    
    # Create logs directory jika tidak ada
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Setup logger
    logger = logging.getLogger('chatbot')
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Format logging
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File Handler dengan rotation
    log_path = f'logs/{LOG_FILE}'
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Initialize logger
logger = setup_logging()
