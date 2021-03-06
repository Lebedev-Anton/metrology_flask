from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from celery import Celery


app = Flask(__name__)
app.config.from_object(Config)
celery_app = Celery(app.name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL']
                    )
celery_app.conf.update(app.config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.entrance'

from web_app.scripts.models import Scripts
from web_app import routes
from web_app.user.models import Users
from web_app.user.views import blueprint as user_blueprint
from web_app.script_runner.views import blueprint as script_runner_blueprint
from web_app.scripts.views import blueprint as script_blueprint
import web_app.admin.views


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


app.register_blueprint(user_blueprint)
app.register_blueprint(script_runner_blueprint)
app.register_blueprint(script_blueprint)
