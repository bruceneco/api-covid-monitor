from app import db
from time import time


class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    creation_date = db.Column(db.BigInteger)

    def __init__(self, name, creation_date=time()):
        self.name = name
        self.creation_date = creation_date

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'creation_date': self.creation_date}

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.to_dict()
        except Exception as e:
            print(e)
            raise Exception('Houve um problema ao cadastrar o sintoma.')

    @classmethod
    def get_by_name(cls, name: str) -> bool:
        try:
            return cls.query.filter_by(name=name).first()
        except Exception as e:
            print(e)
            raise Exception('Houve um problema ao procurar o sintoma.')

    @classmethod
    def get_by_id(cls, _id: int) -> bool:
        try:
            return cls.query.filter_by(id=_id).first()
        except Exception as e:
            print(e)
            raise Exception('Houve um problema ao procurar o sintoma.')

    @classmethod
    def get_all(cls):
        try:
            symptoms = cls.query.all()
            return [{'name': symptom.name, 'creation_date': symptom.creation_date} for symptom in symptoms]

        except Exception as e:
            print(e)
            raise Exception('Houve um problema ao procurar os possíveis sintomas.')
