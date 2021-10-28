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
            return {'message': '"symptom" body param is missing.'}, 400
        elif type(body['symptom']) != str:
            return {'message': '"symptom" body param must be a string.'}, 400
        elif Symptom.get_by_name(name=body['symptom']):
            return {'message': 'Symptom already exists.'}, 403

        symptom = Symptom(body['symptom'])
        return symptom.save(), 201
    except Exception as e:
        print(e)
        return {'message': 'There was an error creating symptom.'}, 500
