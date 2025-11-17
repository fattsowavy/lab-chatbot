"""
Konfigurasi aplikasi chatbot
"""
import os
from datetime import timedelta

# Flask Configuration
DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
TESTING = os.getenv('FLASK_TESTING', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
SESSION_LIFETIME = timedelta(hours=int(os.getenv('SESSION_LIFETIME', '1')))

# Chatbot Configuration
MIN_CONFIDENCE_SCORE = int(os.getenv('MIN_CONFIDENCE', '50'))
MAX_INPUT_LENGTH = int(os.getenv('MAX_INPUT_LENGTH', '500'))
MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_HISTORY', '100'))
KB_FILE = os.getenv('KB_FILE', 'knowledge_base.json')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'chatbot.log')

# Rate limiting
RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT', 'True').lower() == 'true'
MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS', '30'))
