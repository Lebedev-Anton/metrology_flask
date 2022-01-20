from web_app import app
from flask_admin import Admin

admin = Admin(app, name='Metrology', template_mode='bootstrap3', endpoint='admin')

