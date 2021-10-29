from flask import Blueprint, request

from app.decorators.auth import auth_required
from app.models.symptom import Symptom

symptoms = Blueprint(name='symptoms', import_name=__name__, url_prefix='/symptoms')


@symptoms.route('/create', methods=['POST'])
@auth_required(permission_required='admin')
def create_symptom():
    try:
        body = request.json
        if 'symptom' not in body:
            return {'message': 'O parâmetro "symptom" está faltando.'}, 400
        elif type(body['symptom']) != str:
            return {'message': 'O parâmetro "symptom" deve ser uma string.'}, 400
        elif Symptom.get_by_name(name=body['symptom']):
            return {'message': 'Sintoma já existente.'}, 403

        symptom = Symptom(body['symptom'])
        return symptom.save(), 201
    except Exception as e:
        print(e)
        return {'message': 'Houve um problema ao cadastrar o sintoma.'}, 500


@symptoms.route('/', methods=['GET'])
@auth_required(permission_required='default')
def get_symptoms():
    try:
        return {'symptoms': Symptom.get_all()}
    except Exception as e:
        print(e)
        return {'message': 'Houve um problema em procurar todos os sintomas.'}
