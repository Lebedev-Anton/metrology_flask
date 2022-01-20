from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired

from web_app import db
from web_app.user.models import PositionsEmployees
from web_app.user.user_validators import \
    validate_email, validate_username, validate_password, validate_employee_position


class EntranceForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        positions_from_db = db.session.query(PositionsEmployees.position_name).all()
        allowed_position = [position[0] for position in positions_from_db]
        self.employee_position.choices = allowed_position

    username = StringField('Введите имя пользователя',
                           validators=[DataRequired(), validate_username],
                           render_kw={"class": "form-control"})
    password = PasswordField('Введите пароль',
                             validators=[DataRequired(), validate_password],
                             render_kw={"class": "form-control"})
    repeated_password = PasswordField('Повторите пароль',
                                      validators=[DataRequired(), validate_password],
                                      render_kw={"class": "form-control"})

    employee_position = SelectField('Введите должность',
                                    validators=[DataRequired(), validate_employee_position],
                                    render_kw={"class": "form-control"})

    email = EmailField('Введите email',
                       validators=[DataRequired(), validate_email],
                       render_kw={"class": "form-control"})
    submit = SubmitField('Зарегестрироваться', render_kw={"class": "btn btn-primary"})