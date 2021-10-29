from app import db


class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.to_dict()
        except Exception as e:
            print(e)
            raise Exception('Houve um problema ao cadastrar o sintomaÒ.')

    @classmethod
    def get_by_name(cls, name: str) -> bool:
        try:
            return cls.query.filter_by(name=name).first()
        except Exception as e:
            print(e)
            raise Exception('Houve um problema ao procurar o sintoma.')

    @classmethod
    def get_all(cls):
        try:
            symptoms = cls.query.all()
            return [symptom.name for symptom in symptoms]

        except Exception as e:
            print(e)
            raise Exception('Houve um problema ao procurar os possíveis sintomas.')
