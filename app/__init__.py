import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery
from flask import Flask
from flask import request, jsonify
from flask_migrate import Migrate

from app.models import config, db
from app.views import UserView, AdvView

app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRE_URI)
db.init_app(app)
migrate = Migrate(app, db)

celery = Celery(
    app.import_name,
    backend='redis://localhost:49153/1',
    broker='redis://localhost:49153/2'
)
celery.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


@celery.task
@app.route("/", methods=['GET', 'POST'])
def send_emails(mailto):
    mail_params = {
        'host': 'localhost',
        'port': 49155,
        'from': 'test@example.com'
    }

    msg = MIMEMultipart()
    msg['Subject'] = "Test message"
    msg['From'] = mail_params.get('from')
    msg['To'] = mailto

    body = 'This is a test message'

    msg.attach(MIMEText(body, 'plain'))

    host = mail_params.get('host', 'localhost')
    port = mail_params.get('port')
    smtp = smtplib.SMTP(host=host, port=port)
    result = smtp.send_message(msg)
    return result


# appp.add_url_rule('/', view_func=SendMailView.as_view('emails_get'), methods=['GET', ])
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
