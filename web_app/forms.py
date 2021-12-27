from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, ValidationError
from web_app.custom_validators import check_employee_position, check_email_correctness, check_username, check_password
from web_app import db
from web_app.models import PositionsEmployees


def validator(func_to_validate):
    def validate_func(form, field):
        check_status, message = func_to_validate(form, field)
        if not check_status:
            raise ValidationError(message)
    return validate_func


@validator
def validate_username(form, field):
    username = field.data
    check_status, message = check_username(username)
    return check_status, message


@validator
def validate_password(form, field):
    password = field.data
    check_status, message = check_password(password)
    return check_status, message


@validator
def validate_employee_position(form, field):
    employee_position = field.data
    check_status, message = check_employee_position(employee_position)
    return check_status, message


@validator
def validate_email(form, field):
    user_email = field.data
    check_status, message = check_email_correctness(user_email)
    return check_status, message


class SelectScript(FlaskForm):
    select = SubmitField('Подтвердить выбор')


class EntranceForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired(), validate_username])
    password = PasswordField('Введите пароль', validators=[DataRequired(), validate_password])
    repeated_password = PasswordField('Повторите пароль', validators=[DataRequired(), validate_password])

    positions_from_db = db.session.query(PositionsEmployees.position_name).all()
    allowed_position = [position[0] for position in positions_from_db]
    employee_position = SelectField('Введите должность', validators=[DataRequired(), validate_employee_position],
                                    choices=allowed_position)

    email = EmailField('Введите email', validators=[DataRequired(), validate_email])
    submit = SubmitField('Зарегестрироваться')
