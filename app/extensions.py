import os

from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy

from app.settings import PASSWORD_ENCRYPT_KEY

db = SQLAlchemy()
cipher_suite = Fernet(PASSWORD_ENCRYPT_KEY)
jwt_secret = os.getenv('JWT_SECRET')
