from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from web_app import routes, models
from web_app.models import Users
from web_app.user.views import blueprint as user_blueprint

import web_app.admin.views

app.register_blueprint(user_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.entrance'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
