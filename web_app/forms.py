from flask_wtf import FlaskForm
from wtforms import SubmitField

class SelectScript(FlaskForm):
    select = SubmitField('Подтвердить выбор')