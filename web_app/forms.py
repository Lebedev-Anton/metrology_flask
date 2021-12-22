from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, URLField
from wtforms.validators import DataRequired


class SelectScript(FlaskForm):
    select = SubmitField('Подтвердить выбор')


class EntranceForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    registration = URLField('регистрация')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    repeated_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    employee_position = StringField('Введите должность', validators=[DataRequired()])
    email = StringField('Введите email', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
