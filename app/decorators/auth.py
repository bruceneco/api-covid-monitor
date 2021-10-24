from flask import request

from app.settings import PERMISSIONS_CODE_MAP
from app.utils.auth import decode_token


def auth_required(permission_required='default'):
    def decorator(function):
        def validate_permissions(*args, **kwargs):
            token = request.headers.get('Authorization')
            message = 'You are not logged in.'
            if token:
                message = 'Invalid token.'
                user = decode_token(token)
                if user and user['permission'] >= PERMISSIONS_CODE_MAP[permission_required]:
                    return function(*args, **kwargs)
                else:
                    message = 'You do not have enough permissions.'
            
            return {"message": message}, 403

        validate_permissions.__name__ = function.__name__
        return validate_permissions

    return decorator
