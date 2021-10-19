from app.app import cipher_suite, jwt_secret, admin_key, db, app
from app.models.user import User
import jwt
from flask import request


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
