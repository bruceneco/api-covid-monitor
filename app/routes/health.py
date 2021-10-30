from flask import Blueprint, request

from app.decorators.auth import auth_required
from app.models.health import Health
from app.models.symptom import Symptom
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

        symptom_ids = [Symptom.get_by_name(symptom).id for symptom in body['symptoms']]

        if Health.check_day_registry(body['date'], user_code):
            return {'message': 'Registro já feito hoje.'}, 400

        health_registries = []
        if len(symptom_ids):
            for symptom in symptom_ids:
                health_registry = Health(date=body['date'], user=user_code, symptom=symptom)
                health_registries.append(health_registry)
            Health.save_all(health_registries)
        else:
            Health(date=body['date'], symptom=None, user=user_code).save()
            return {'message': 'Estado "saudável" cadastrado.'}, 201

        return {'message': "Sintomas cadastrados"}, 201

    except Exception as e:
        return {'message': str(e)}, 500
