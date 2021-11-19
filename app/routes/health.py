from flask import Blueprint, request

from app.decorators.auth import auth_required
from app.models.health import Health
from app.models.symptom import Symptom
from app.utils.auth import decode_token, get_user

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


@health.route('/report', methods=['GET'])
@auth_required(permission_required='hr')
def get_report():
    try:
        args = request.args
        try:
            int(args['initial_date'])
            int(args['final_date'])
        except:
            raise Exception('Os timestamps devem ser conversíveis para inteiro.')

        if "initial_date" not in args or "by_sector" not in args or "final_date" not in args:
            return {'message': "Parâmetros inválidos."}, 400
        elif int(args['initial_date']) >= int(args['final_date']):
            return {"message": "Período inválido."}, 400
        try:
            if "False" != args['by_sector'] != "True":
                raise Exception()
        except:
            raise Exception("A opção de ser por setor deve ser 'True' ou 'False'.")

        transformed_body = {
            'by_sector': args['by_sector'] == "True",
            'initial_date': int(args['initial_date']),
            'final_date': int(args['final_date']),
        }
        if transformed_body['by_sector']:
            count = Health.count_health_status_by_sector(transformed_body['initial_date'],
                                                         transformed_body['final_date'])
            if not count:
                return {'message': "Sem registros."}, 404
            return count, 200
        else:
            count = Health.count_health_status(transformed_body['initial_date'], transformed_body['final_date'])
            if not count:
                return {'message': "Sem registros."}, 404
            return count, 200
    except Exception as e:
        return {'message': str(e)}, 500


@health.route('/frequency', methods=['GET'])
@auth_required('hr')
def get_frequency():
    try:
        args = request.args
        try:
            initial_ts = int(args['initial_date'])
            final_ts = int(args['final_date'])
        except:
            return {'message': 'Parâmetros inválidos.'}, 400
        if initial_ts >= final_ts:
            return {'message': 'Período inválido.'}, 400
        result = Health.get_frequency_by_period(initial_ts, final_ts)
        return result, 200
    except Exception as e:
        return {'message': str(e)}, 500


@health.route('/history', methods=['GET'])
@auth_required()
def get_history():
    try:
        user = get_user()
        health_registries = Health.get_all_by_user(code=user['code'])
        registries_by_day = {}
        for health_registry in health_registries:
            if health_registry.date not in registries_by_day:
                registries_by_day[health_registry.date] = []
            if health_registry.symptom:
                registries_by_day[health_registry.date].append(Symptom.get_by_id(health_registry.symptom).name)
        return registries_by_day, 200
    except Exception as e:
        return {'message': str(e)}, 500
