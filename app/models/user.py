from app.extensions import db


class User(db.Model):
    code = db.Column(db.String, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String, nullable=False)
    uf = db.Column(db.String, nullable=False)
    sector = db.Column(db.String, nullable=True)

    def __init__(self, code, full_name, password, birth_date, city, uf, sector=None):
        self.code = code
        self.full_name = full_name
        self.password = password
        self.birth_date = birth_date
        self.city = city
        self.uf = uf
        self.sector = sector

    def to_dict(self):
        obj_dict = {
            'code': self.code,
            'full_name': self.full_name,
            'password': self.password,
            'birth_date': self.birth_date,
            'city': self.city,
            'uf': self.uf,
        }
        if self.sector:
            obj_dict['sector'] = self.sector
        return obj_dict
