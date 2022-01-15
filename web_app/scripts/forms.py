from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired


class ShowMessageForm(FlaskForm):
    submit = SubmitField('Ок')


class ShowQuestionForm(FlaskForm):
    def __init__(self, user_choice, **kwargs):
        super().__init__(**kwargs)
        self.choice.choices = user_choice.split(';')
    choice = SelectField(validators=[DataRequired()])
    submit = SubmitField('Ок')


class ShowNumberForm(FlaskForm):
    number = DecimalField(validators=[DataRequired()])
    submit = SubmitField('Ок')