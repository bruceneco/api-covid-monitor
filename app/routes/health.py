from flask import Blueprint, request

from app.decorators.auth import auth_required
from app.models.health import Health
from app.models.symptom import Symptom
from app.models.user import User
from app.utils.auth import decode_token

health = Blueprint('health', import_name=__name__, url_prefix='/health')


@health.route('/register', methods=['POST'])
@auth_required(permission_required='default')
def register_health():
    try:

        body = request.json
        user_code = decode_token(request.headers.get('Authorization'))['code']

        if not body.get('date') or 'symptoms' not in body:
            return {'message': 'Faltam parâmetros.'}, 400
        elif None in [Symptom.get_by_name(symptom) for symptom in body['symptoms']]:
            return {'message': 'Sintoma inexistente.'}, 400
        elif not len(body['symptoms']):
            return {'message': 'Não há sintomas para cadastrar.'}, 200

        symptom_ids = [Symptom.get_by_name(symptom).id for symptom in body['symptoms']]
        n_registry_added = len(symptom_ids)
        health_registries = []

        for symptom in symptom_ids:
            health_registry = Health(date=body['date'], user=user_code, symptom=symptom)
            if health_registry.check_already_exists():
                n_registry_added -= 1
                continue
            health_registries.append(health_registry)
        Health.save_all(health_registries)

        if n_registry_added == len(symptom_ids):
            return {'message': "Sintomas cadastrados"}, 201
        elif n_registry_added == 0:
            return {'message': 'Registros já feitos hoje.'}, 400
        else:
            return {'message': 'Sintomas parcialmente cadastrados.'}, 202

    except Exception as e:
        return {'message': str(e)}, 500
