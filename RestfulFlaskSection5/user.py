import sqlite3
from db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, _id, username, password):
        self.id = _id
        self.name = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(name=username).first()
        return user

    @classmethod
    def find_by_id(cls, _id):
        user = cls.query.filter_by(id=_id).first()
        return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print(User.find_by_username(self.name))
