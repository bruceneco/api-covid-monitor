from app.extensions import db


class User(db.Model):
    code = db.Column(db.String, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Integer)
    city = db.Column(db.String)
    uf = db.Column(db.String)
    sector = db.Column(db.String)
    permission = db.Column(db.Integer, default=0)

    def __init__(self, code, full_name, password, birth_date, city, uf, sector, permission):
        self.code = code
        self.full_name = full_name
        self.password = password
        self.birth_date = birth_date
        self.city = city
        self.uf = uf
        self.sector = sector
        self.permission = permission

    def to_dict(self):
        obj_dict = {
            'code': self.code,
            'full_name': self.full_name,
            'password': self.password,
            'birth_date': self.birth_date,
            'city': self.city,
            'uf': self.uf,
            'permission': self.permission,
        }
        if self.sector:
            obj_dict['sector'] = self.sector
        return obj_dict

    @classmethod
    def get_user(cls, code):
        code = str(code)
        return cls.query.filter_by(code=code).first()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.to_dict()
        except Exception:
            raise Exception("Error on saving user to database.")