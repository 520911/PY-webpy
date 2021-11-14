from datetime import datetime

import gino
from aiohttp import web

db = gino.Gino()


class NotFound(Exception):
    pass


@web.middleware
async def not_found_handler(request, handler):
    try:
        response = await handler(request)
    except NotFound:
        response = web.json_response({'error': ' Not found'}, status=404)
    return response


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Adv(db.Model):
    __tablename__ = 'adv'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date_posted': str(self.date_posted),
            'content': self.content,
            'user_id': self.user_id
        }
