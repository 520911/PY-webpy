import hashlib
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import config


db = SQLAlchemy()


class BaseModelMixin:

    def add(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    adv = db.relationship('Adv', backref='author', lazy=True)

    def __str__(self):
        return f'User: {self.username}, email: {self.email}'

    def __repr__(self):
        return f'User: {self.username}, email: {self.email}'

    def set_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Adv(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f'Adv: {self.title}, title: {self.date_posted}'

    def __repr__(self):
        return f'Adv: {self.title}, title: {self.date_posted}'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date_posted,
            'user': self.user_id
        }
