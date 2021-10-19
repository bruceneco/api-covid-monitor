from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from cryptography.fernet import Fernet
from flask import Flask
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('APP_SECRET_KEY')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = os.getenv('CUSTOM_DB_URL')
db = SQLAlchemy(app)
db.create_all()
cipher_suite = Fernet(os.getenv('PASSWORD_ENCRYPT_KEY'))
migrate = Migrate(app, db)
jwt_secret = os.getenv('JWT_SECRET')
admin_key = 'admin_key'


if __name__ == '__main__':
    app.run()
