from sqlalchemy import Column, String
from .shared import declarative_base, db


class ApiKeyModel(declarative_base):
    __tablename__ = 'api_keys'

    def __init__(self, name, key):
        self.name = name
        self.key = key

    domain = Column(String, unique=True, primary_key=True)
    key = Column(String)

    @staticmethod
    def list():
        keys = ApiKeyModel.query.all()
        out = {}

        for k in keys:
            out[k.name] = k.key

        return out

    @staticmethod
    def get(name):
        return ApiKeyModel.query \
                   .filter_by(domain=name.upper()) \
                   .first()

    @staticmethod
    def set(name, key):
        try:
            key_value = ApiKeyModel.get(name)
            if key_value is None:
                ApiKeyModel.add(name, key)
            else:
                ApiKeyModel.update.where(name=name.upper()).values(key=key)
                db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def add(name, key):
        try:
            db.session.add(ApiKeyModel(name.upper(), key=key))
            db.session.commit()
            return True
        except:
            return False

    @staticmethod
    def remove(name):
        try:
            ApiKeyModel.query.filter_by(name=name.upper()).remove()
            db.session.commit()
            return True
        except:
            return False
