import os

from dotenv import load_dotenv

load_dotenv(
    dotenv_path=".env"
)

# Telegram Bot Settings
DEVELOPER = os.getenv('DEVELOPER')
DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG')
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS').split(',') if host]

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_STORAGE_CHAT_ID = os.getenv('TELEGRAM_STORAGE_CHAT_ID')

BASE_WEBHOOK_URL = os.getenv('BASE_WEBHOOK_URL')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
WEB_SERVER_PORT = int(os.getenv('WEB_SERVER_PORT'))
WEB_SERVER_HOST = os.getenv('WEB_SERVER_HOST')
WEBHOOK_PATH = '/bot/webhook/'

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')