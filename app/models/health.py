from app import db


class Health(db.Model):
    date = db.Column(db.BigInteger, primary_key=True)
    symptom = db.Column(db.Integer, db.ForeignKey('symptom.id'), primary_key=True)
    user = db.Column(db.String, db.ForeignKey('user.code'), primary_key=True)

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

    def check_already_exists(self):
        return Health.query.filter_by(date=self.date, symptom=self.symptom, user=self.user).first()

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
