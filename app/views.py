from flask import request, jsonify
from flask.views import MethodView

from app.models import User


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
        response.status_code = 200
        return response

    def post(self):
        user = User(**request.json)
        user.set_password(request.json['password'])
        user.add()
        return jsonify(user.to_dict())
