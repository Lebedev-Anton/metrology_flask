from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user
from web_app import db
from web_app.scripts.forms import ShowMessageForm, ShowQuestionForm
from web_app.script_runner.models import CheckedPointData

from flask import Blueprint
blueprint = Blueprint('script', __name__, url_prefix='/script')


@blueprint.route('/show_message/<message>-<checked_point_id>-<path>')
def show_message(message, checked_point_id, path):
    if current_user.is_authenticated:
        form = ShowMessageForm()
        return render_template('scripts/show_message.html', message=message,
                               form=form, checked_point_id=checked_point_id, path=path)
    return redirect(url_for('index'))


@blueprint.route('/process-show_message/<checked_point_id>-<path>', methods=['POST'])
def processing_show_message(checked_point_id, path):
    form = ShowMessageForm()
    submit = str(form.submit.data)
    checked_point_data = CheckedPointData.query.filter_by(
        id_checked_point=checked_point_id).order_by(CheckedPointData.id.desc()).first()
    checked_point_data.user_answer = submit
    db.session.commit()
    return redirect(url_for('script_runner.run_script', checked_point_id=checked_point_id, path=path))


@blueprint.route('/show_question/<message>-<choice>-<checked_point_id>-<path>')
def show_question(message, choice, checked_point_id, path):
    if current_user.is_authenticated:
        form = ShowQuestionForm(choice)
        return render_template('scripts/show_question.html', message=message, choice=choice,
                               form=form, checked_point_id=checked_point_id, path=path)
    return redirect(url_for('index'))


@blueprint.route('/process-show_question/<choice>-<checked_point_id>-<path>', methods=['POST'])
def processing_show_question(choice, checked_point_id, path):
    form = ShowQuestionForm(choice)
    choice = str(form.choice.data)
    submit = str(form.submit.data)
    user_answer = str({'choise': choice, 'submit': submit})
    checked_point_data = CheckedPointData.query.filter_by(
        id_checked_point=checked_point_id).order_by(CheckedPointData.id.desc()).first()
    checked_point_data.user_answer = user_answer
    db.session.commit()
    return redirect(url_for('script_runner.run_script', checked_point_id=checked_point_id, path=path))
