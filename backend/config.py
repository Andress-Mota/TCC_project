import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_CONFIG = {
    'host':     os.getenv('DB_HOST',     'localhost'),
    'user':     os.getenv('DB_USER',     'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME',     'tcc_imagens'),
}

SECRET_KEY         = os.getenv('SECRET_KEY',         'dev-secret-key')
FERNET_KEY         = os.getenv('FERNET_KEY',         '')
GMAIL_SENDER       = os.getenv('GMAIL_SENDER',       '')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
