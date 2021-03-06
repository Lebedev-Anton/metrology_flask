from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, EmailField, SelectField, SelectMultipleField, DateField
from wtforms.validators import DataRequired

from web_app import db
from web_app.admin.models import WorkType, AccessRights
from web_app.user.models import PositionsEmployees, Users
from web_app.user.user_validators import \
    validate_email, validate_username, validate_password, validate_employee_position, validate_responsible_user


def get_users_from_db():
    users_from_db = db.session.query(Users.username).all()
    users = [user[0] for user in users_from_db]
    return users


def get_work_types_from_db():
    work_types_from_db = db.session.query(WorkType.work_type_name).all()
    allowed_work_types = [work_type[0] for work_type in work_types_from_db]
    return allowed_work_types


def get_allowed_position():
    positions_from_db = db.session.query(PositionsEmployees.position_name).all()
    allowed_position = [position[0] for position in positions_from_db]
    return allowed_position


class EditUserFrom(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired()])

    employee_position = SelectField('Введите должность', validators=[DataRequired(), validate_employee_position],
                                    choices=lambda: get_allowed_position())
    allowed_work_types = SelectMultipleField('Выберете допустимые виды работ', choices=lambda: get_work_types_from_db())

    email = EmailField('Введите email', validators=[DataRequired(), validate_email])


class RegistrationForm(EditUserFrom):
    username = StringField('Введите имя пользователя', validators=[DataRequired(), validate_username])
    password = PasswordField('Введите пароль', validators=[DataRequired(), validate_password])
    repeated_password = PasswordField('Повторите пароль', validators=[DataRequired(), validate_password])


class DevicesForm(FlaskForm):
    serial_number = StringField('Введите серийный номер', validators=[DataRequired()])
    order_number = StringField('Введите номер заявки', validators=[DataRequired()])
    modification = StringField('Введите модификацию', validators=[DataRequired()])
    delivery_date = DateField('Введите дату поступления', validators=[DataRequired()])

    work_type = SelectField('Выберете вид работ', validators=[DataRequired()],
                            choices=lambda: get_work_types_from_db())


class WorkStatusForm(FlaskForm):
    order_number = StringField('Введите номер заявки', validators=[DataRequired()])
    user = SelectField('Выберете исполнителя', validators=[DataRequired(), validate_responsible_user],
                       choices=lambda: get_users_from_db())

    work_status = SelectField('Выберете статут работ', validators=[DataRequired()],
                              choices=['backlog', 'progress', 'done'])
