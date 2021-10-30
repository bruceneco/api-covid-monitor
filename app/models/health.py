from app import db


class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.BigInteger)
    symptom = db.Column(db.Integer, db.ForeignKey('symptom.id'), nullable=True)
    user = db.Column(db.String, db.ForeignKey('user.code'))

    def __init__(self, date, symptom, user):
        self.date = date
        self.symptom = symptom
        self.user = user

    def to_dict(self):
        return {
            'date': self.date,
            'symptom': self.symptom,
            'user': self.user,
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.to_dict()
        except Exception as e:
            print(e)
            raise Exception('Houve um problema ao salvar o registro de saúde.')

    @classmethod
    def save_all(cls, list_of_health):
        try:
            db.session.add_all(list_of_health)
            db.session.commit()
        except Exception as e:
            print(e)
            raise Exception("Houve um problema ao salvar os sintomas.")

    @classmethod
    def check_day_registry(cls, date, user_code):
        try:
            return cls.query.filter_by(date=date, user=user_code).first()
        except Exception as e:
            print(e)
            raise Exception(e)
