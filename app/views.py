from celery.result import AsyncRusult
from flask import request, jsonify
from flask.views import MethodView
from flask_httpauth import HTTPBasicAuth

from __init__ import send_emails, celery
from app.models import User, Adv

auth = HTTPBasicAuth()


class UserView(MethodView):

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            response = jsonify(
                {
                    'error': 'User not found'
                }
            )
            response.status_code = 404
            return response
        response = jsonify(user.to_dict())
        return response

    def post(self):
        user = User(**request.json)
        user.set_password(request.json['password'])
        user.add()
        return jsonify(user.to_dict())


class AdvView(MethodView):

    def get(self, adv_id):
        adv = Adv.query.get(adv_id)
        if not adv:
            response = jsonify(
                {
                    'error': 'Adv not found'
                }
            )
            response.status_code = 404
            return response
        else:
            response = jsonify(adv.to_dict())
            return response

    @auth.login_required
    def post(self):
        adv = Adv(**request.json)
        user_name = request.authorization.username
        adv.user_id = User.query.filter_by(username=user_name).first().id
        adv.add()
        return jsonify(adv.to_dict())

    @auth.login_required
    def delete(self, adv_id):
        adv = Adv.query.filter_by(id=adv_id).first()
        user_name = request.authorization.username
        user_id = User.query.filter_by(username=user_name).first().id
        if adv and user_id == adv.user_id:
            Adv.query.filter_by(id=adv_id).delete()
            adv.commit()
            return jsonify(
                {
                    'status': 'removed',
                    'adv_id': adv_id
                }
            )
        else:
            return jsonify({'error': 'Adv does not exist or not get permission'})

    @auth.login_required
    def patch(self, adv_id):
        adv = Adv.query.filter_by(id=adv_id).first()
        user_name = request.authorization.username
        user_id = User.query.filter_by(username=user_name).first().id
        adv.title = request.json.get('title')
        adv.content = request.json.get('content')
        if adv and user_id == adv.user_id:
            adv.commit()
            return jsonify(
                {
                    'status': 'patched',
                    'adv_id': adv_id
                }
            )
        else:
            return jsonify({'error': 'Adv does not exist or not get permission'})

    @staticmethod
    @auth.verify_password
    def verify_password(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return False
        return True


class SendMailView(MethodView):
    def get(self, task_id):
        task = AsyncRusult(task_id, app=celery)
        return jsonify({
            'status': task.status,
            'result': task.result
        })

    def post(self):
        emails = [*User.query.all().emails]
        task = send_emails.delay(*emails)
        return jsonify({'task_id': task.id})
