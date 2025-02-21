import os
from dotenv import load_dotenv

load_dotenv()

# set up host url
BASE_URL = 'http://127.0.0.1:8000'

# set up data for connecting to the database
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

DB_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

# catalogs for media data
# created in the root dir
UPLOAD_DIR = "uploads"
POSTS_IMAGES_DIR = f'{UPLOAD_DIR}/posts'

# set up data for authentication
AUTH_KEY = os.getenv('AUTH_KEY')
HASHING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

ALLOWED_HOSTS = [
    'http://localhost:3000',
    'http://127.0.0.1:8000'
]