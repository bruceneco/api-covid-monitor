import jwt
from flask import request

from app.extensions import jwt_secret


def decode_token(token):
    try:
        return jwt.decode(token, jwt_secret)
    except:
        return None


def get_user():
    token = request.headers.get('Authorization')
    return decode_token(token)
