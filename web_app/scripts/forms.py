from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired


class ShowMessageForm(FlaskForm):
    submit = SubmitField('Ок', render_kw={"class": "btn btn-primary"})


class ShowQuestionForm(FlaskForm):
    def __init__(self, user_choice, **kwargs):
        super().__init__(**kwargs)
        self.choice.choices = user_choice.split(';')
    choice = SelectField(validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Ок', render_kw={"class": "btn btn-primary"})


class ShowNumberForm(FlaskForm):
    number = DecimalField(validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Ок', render_kw={"class": "btn btn-primary"})
