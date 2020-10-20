import sqlite3
from db import db


class Store(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, _id, name):
        self.id = _id
        self.name = name


    @classmethod
    def find_by_name(cls, name):
        user = cls.query.filter_by(name=name).first()
        return user

    @classmethod
    def find_by_id(cls, _id):
        user = cls.query.filter_by(id=id).first()
        return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

