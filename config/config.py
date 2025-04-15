import os
from dotenv import load_dotenv
from datetime import timedelta
from app.config.keys import JWT_PUBLIC_KEY


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'), override=True)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_PUBLIC_KEY = JWT_PUBLIC_KEY  # Set the public key for RS256
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ALGORITHM = 'RS256'  # Specify the algorithm
    JWT_DECODE_ALGORITHMS = ['RS256']  # List of allowed algorithms

    uri = os.environ.get("DATABASE_URL")  # or other relevant config var
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri