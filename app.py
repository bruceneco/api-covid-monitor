from flask import Flask, request
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
from cryptography.fernet import Fernet

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
cipher_suite = Fernet(os.getenv('PASSWORD_ENCRYPT_KEY'))
migrate = Migrate(app, db)
jwt_secret = os.getenv('JWT_SECRET')
admin_key = 'admin_key'


class User(db.Model):
    code = db.Column(db.String, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String, nullable=False)
    uf = db.Column(db.String, nullable=False)
    sector = db.Column(db.String, nullable=True)

    def __init__(self, code, full_name, password, birth_date, city, uf, sector=None):
        self.code = code
        self.full_name = full_name
        self.password = password
        self.birth_date = birth_date
        self.city = city
        self.uf = uf
        self.sector = sector

    def to_dict(self):
        obj_dict = {
            'code': self.code,
            'full_name': self.full_name,
            'password': self.password,
            'birth_date': self.birth_date,
            'city': self.city,
            'uf': self.uf,
        }
        if self.sector:
            obj_dict['sector'] = self.sector
        return obj_dict


@app.route('/register', methods=["POST"])
def register_member():
    body = request.json
    if body['admin_key'] != admin_key:
        return {'message': 'Invalid key'}, 401
    if 'code' not in body \
            or 'password' not in body \
            or 'full_name' not in body \
            or 'password' not in body \
            or 'birth_date' not in body \
            or 'city' not in body \
            or 'uf' not in body:
        return {'message': 'Invalid params'}, 400
    if User.query.filter_by(code=body['code']).first():
        return {'message': 'User already exists'}, 400
    new_user = User(code=body['code'], full_name=body['full_name'],
                    password=cipher_suite.encrypt(bytes(body['password'], 'utf-8')).decode('utf-8'),
                    birth_date=body['birth_date'], city=body['city'], uf=body['uf'])
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()


@app.route('/auth', methods=['POST'])
def authenticate():
    body = request.json
    if 'code' not in body or 'password' not in body:
        return {'message': 'Invalid credendials'}, 400
    if not User.query.filter_by(code=body['code']).first():
        return {'message': 'User not found'}, 404

    user = User.query.filter_by(code=body['code']).first().to_dict()
    decrypted_password = cipher_suite.decrypt(bytes(user['password'], 'utf-8')).decode('utf-8')

    if body['password'] != decrypted_password:
        return {'message': 'Invalid password'}, 401

    del user['birth_date']
    token = jwt.encode(user, jwt_secret).decode('utf-8')
    return {'token': token}, 200

@app.route('/checkToken', methods=['POST'])
def check_token():
    body = request.json
    return jwt.decode(body['token'], jwt_secret)

if __name__ == '__main__':
    app.run(debug=True)
