import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

DB_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

BASE_URL = 'http://127.0.0.1:8000'

AUTH_KEY = os.getenv('AUTH_KEY')

UPLOAD_DIR = "uploads"

POSTS_IMAGES_DIR = f'{UPLOAD_DIR}/posts'