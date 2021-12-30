from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired

from web_app import db
from web_app.user.models import PositionsEmployees
from web_app.user.user_validators import \
    validate_email, validate_username, validate_password, validate_employee_position


class RegistrationForm(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired(), validate_username])
    password = PasswordField('Введите пароль', validators=[DataRequired(), validate_password])
    repeated_password = PasswordField('Повторите пароль', validators=[DataRequired(), validate_password])

    positions_from_db = db.session.query(PositionsEmployees.position_name).all()
    allowed_position = [position[0] for position in positions_from_db]
    employee_position = SelectField('Введите должность', validators=[DataRequired(), validate_employee_position],
                                    choices=allowed_position)

    email = EmailField('Введите email', validators=[DataRequired(), validate_email])


class EditUserFrom(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired(), validate_username])
    positions_from_db = db.session.query(PositionsEmployees.position_name).all()
    allowed_position = [position[0] for position in positions_from_db]
    employee_position = SelectField('Введите должность', validators=[DataRequired(), validate_employee_position],
                                    choices=allowed_position)

    email = EmailField('Введите email', validators=[DataRequired(), validate_email])