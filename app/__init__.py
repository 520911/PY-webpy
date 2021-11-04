from flask import Flask
from flask import request, jsonify
from flask_migrate import Migrate
from app.models import config, db
from app.views import UserView, AdvView

app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRE_URI)
db.init_app(app)
migrate = Migrate(app, db)

app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_get'), methods=['GET', ])
app.add_url_rule('/users/', view_func=UserView.as_view('users_create'), methods=['POST', ])

app.add_url_rule('/adv/<int:adv_id>', view_func=AdvView.as_view('adv_get'), methods=['GET', ])
app.add_url_rule('/adv/', view_func=AdvView.as_view('adv_create'), methods=['POST', ])
app.add_url_rule('/adv/<int:adv_id>', view_func=AdvView.as_view('adv_delete'), methods=['DELETE', ])
app.add_url_rule('/adv/<int:adv_id>', view_func=AdvView.as_view('adv_patch'), methods=['PATCH', ])


@app.route('/health/', methods=['GET', ])
def health():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})

    return {'status': 'OK'}
