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
            raise Exception('There was an error inserting symptom into database.')

    @classmethod
    def get_by_name(cls, name: str) -> bool:
        try:
            return cls.query.filter_by(name=name).first()
        except Exception as e:
            print(e)
            raise Exception('There was an error during get symptom.')
