import os
from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv('API_HOST')
API_PORT = int(os.getenv('API_PORT'))
API_VERSION = os.getenv('API_VERSION')

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

REDIS_USER = os.getenv('REDIS_USER')
REDIS_PASS = os.getenv('REDIS_PASS')

REAL_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
