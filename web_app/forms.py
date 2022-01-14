from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from web_app.models import Scripts, Devices, WorkStatus
from web_app import db


class SelectScript(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        order_numbers = db.session.query(Devices.order_number).join(WorkStatus).filter(
            WorkStatus.user_id == current_user.id).all()
        self.order_number.choices = [order_number[0] for order_number in order_numbers]

    scripts_from_db = Scripts.query.all()
    scripts = [script.script_name for script in scripts_from_db]
    script = SelectField('Выберете скрипт', validators=[DataRequired()], choices=scripts)
    select = SubmitField('Подтвердить выбор')
    order_number = SelectField('Выберете вид работ', validators=[DataRequired()])


