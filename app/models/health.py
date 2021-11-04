from app import db
from app.models.user import User


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

    @classmethod
    def get_all_by_sector(cls, start_date=0, final_date=999999999999):
        try:
            query_result = db.session.query(Health, User) \
                .filter(Health.user == User.code, User.sector != None, start_date <= Health.date,
                        Health.date <= final_date).distinct(
                Health.user, Health.date).all()
            sectors = {}
            for health_registry, user in query_result:
                if (user.sector not in sectors):
                    sectors[user.sector] = []
                sectors[user.sector].append(health_registry)
            return sectors if sectors else None
        except Exception as e:
            print(e)
            raise Exception(e)

    @classmethod
    def get_all(cls, start_date=0, final_date=999999999999):
        try:
            query_result = db.session.query(Health, User) \
                .filter(Health.user == User.code, start_date <= Health.date,
                        Health.date <= final_date).distinct(
                Health.user, Health.date).all()
            result = [health_registry for health_registry, _ in query_result]
            return result if result else None
        except Exception as e:
            print(e)
            raise Exception(e)

    @classmethod
    def count_health_status_by_sector(cls, initial_date, final_date):
        registries_by_sector = cls.get_all_by_sector(initial_date, final_date)
        if not registries_by_sector:
            return None
        registries_by_day_and_sector = {}
        for sector in registries_by_sector:
            for health_registry in registries_by_sector[sector]:
                date = health_registry.date
                if date not in registries_by_day_and_sector:
                    registries_by_day_and_sector[date] = {}
                if sector not in registries_by_day_and_sector[date]:
                    registries_by_day_and_sector[date][sector] = {'healthy': 0, 'unhealthy': 0}
                if health_registry.symptom:
                    registries_by_day_and_sector[date][sector]['unhealthy'] += 1
                else:
                    registries_by_day_and_sector[date][sector]['healthy'] += 1
        return registries_by_day_and_sector

    @classmethod
    def count_health_status(cls, initial_date, final_date):
        registries = cls.get_all(initial_date, final_date)
        if not registries:
            return None
        registries_by_day = {}
        for health_registry in registries:
            date = health_registry.date
            if date not in registries_by_day:
                registries_by_day[date] = {'healthy': 0, 'unhealthy': 0}
            if health_registry.symptom:
                registries_by_day[date]['unhealthy'] += 1
            else:
                registries_by_day[date]['healthy'] += 1
        return registries_by_day

    @classmethod
    def get_frequency_by_period(cls, initial_ts, final_ts):
        try:
            result = cls.query.filter(cls.date >= initial_ts, cls.date <= final_ts).distinct(cls.date, cls.user).all()
            users_frequency = {}
            for health_registry in result:
                user_code = health_registry.user
                if user_code not in users_frequency:
                    users_frequency[user_code] = 0
                users_frequency[user_code] += 1
            return users_frequency
        except Exception as e:
            print(e)
            raise e

    @classmethod
    def get_all_by_user(cls, code):
        try:
            query_result = cls.query.filter(cls.user == code).all()
            return query_result
        except Exception as e:
            print(e)
            raise e
