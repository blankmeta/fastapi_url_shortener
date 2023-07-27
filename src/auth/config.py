import os

SECRET_KEY = os.getenv('SECRET', 'secret_key')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
