from flask import Blueprint

from app.decorators.auth import auth_required
from app.models.user import User

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/all', methods=['GET'])
@auth_required('hr')
def get_all_users():
    try:
        return {'users': [{'code': usr.code, 'name': usr.full_name, 'sector': usr.sector} for usr in
                          User.get_all()]}, 200
    except Exception as e:
        return {'message': str(e)}, 500
