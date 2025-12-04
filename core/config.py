import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

DEVELOPER = os.getenv('DEVELOPER')
DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

allowed_hosts = os.getenv('ALLOWED_HOSTS')
if allowed_hosts:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(',') if host]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_STORAGE_CHAT_ID = os.getenv('TELEGRAM_STORAGE_CHAT_ID')

BASE_WEBHOOK_URL = os.getenv('BASE_WEBHOOK_URL')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
WEB_SERVER_PORT = int(os.getenv('WEB_SERVER_PORT', '8000'))
WEB_SERVER_HOST = os.getenv('WEB_SERVER_HOST', '0.0.0.0')
WEBHOOK_PATH = '/bot/webhook/'

DB_NAME = os.getenv('DB_NAME', 'lesailes_db')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', '')