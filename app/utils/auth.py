import jwt

from app.extensions import jwt_secret


def decode_token(token):
    try:
        return jwt.decode(token, jwt_secret)
    except:
        return None
