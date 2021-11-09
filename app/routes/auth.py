import jwt
from flask import request, Blueprint

from app.decorators.auth import auth_required
from app.extensions import jwt_secret
from app.models.user import User
from app.utils.auth import decode_token
from app.utils.cypher import encode_password, decode_password

auth = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
def authenticate():
    body = request.json
    body['code'] = str(body['code'])
    if 'code' not in body or 'password' not in body:
        return {'message': 'Invalid credentials'}, 400
    if not User.query.filter_by(code=body['code']).first():
        return {'message': 'User not found'}, 404

    user = User.get_user(body['code']).to_dict()
    decrypted_password = decode_password(user['password'])

    if body['password'] != decrypted_password:
        return {'message': 'Invalid password'}, 401

    del user['birth_date']
    token = jwt.encode(user, jwt_secret).decode('utf-8')
    return {'token': token, 'permission': user['permission']}, 200


@auth.route('/register', methods=["POST"])
@auth_required(permission_required='admin')
def register_member():
    try:
        body = request.json
        if 'code' not in body \
                or 'password' not in body \
                or 'full_name' not in body:
            return {'message': 'Invalid params'}, 400

        if User.get_user(code=body['code']):
            return {'message': 'User already exists'}, 400

        new_user = User(code=body['code'], full_name=body['full_name'],
                        password=encode_password(body['password']),
                        birth_date=body['birth_date'] if 'birth_date' in body else None,
                        city=body['city'] if 'city' in body else None,
                        uf=body['uf'] if 'uf' in body else None,
                        sector=body['sector'] if 'sector' in body else None,
                        permission=body['permission'] if 'permission' in body else None)
        return new_user.save(), 201
    except Exception as e:
        print(e)
        return {'message': 'There was an error creating user'}, 500


@auth.route('/changePassword', methods=['POST'])
@auth_required()
def change_password():
    try:
        body = request.json
        if 'old_password' not in body \
                or 'new_password' not in body:
            return {'message': 'Invalid params'}, 400
        user_data = decode_token(request.headers.get('Authorization'))
        if decode_password(user_data['password']) == body['old_password']:
            new_user = User.get_user(user_data['code'])
            new_user.password = encode_password(body['new_password'])
            new_user.save()
        else:
            return {'message': 'Invalid old password.'}, 403
        return {'message': 'Password changed.'}, 200
    except Exception as e:
        print(e)
        return {'message': 'There was an error updating password.'}, 500
