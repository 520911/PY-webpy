from flask import Flask

from flask_migrate import Migrate
from app.models import config, db

app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRE_URI)
db.init_app(app)
migrate = Migrate(app, db)
