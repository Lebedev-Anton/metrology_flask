from flask import render_template, url_for, redirect
from flask_login import current_user, login_required
from web_app import db
from web_app.scripts.forms import ShowMessageForm, ShowQuestionForm, ShowNumberForm
from web_app.script_runner.models import CheckedPointData
from web_app.script_runner.enums import Status
from flask import Blueprint
from web_app.scripts.validators import is_allowed_to_this_work

blueprint = Blueprint('script', __name__, url_prefix='/script')


@login_required
@blueprint.route('/show_message/<checked_point_id>')
def show_message(checked_point_id):
    if is_allowed_to_this_work(checked_point_id):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=checked_point_id).order_by(CheckedPointData.id.desc()).first()
        page_content = eval(checked_point_data.page_content)
        message = page_content['message']
        path = page_content['path']
        form = ShowMessageForm()
        return render_template('scripts/show_message.html', message=message,
                               form=form, checked_point_id=checked_point_id, path=path)
    return redirect(url_for('index'))


@login_required
@blueprint.route('/process-show_message/<checked_point_id>-<path>', methods=['POST'])
def processing_show_message(checked_point_id, path):
    if is_allowed_to_this_work(checked_point_id):
        form = ShowMessageForm()
        submit = str(form.submit.data)
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=checked_point_id).order_by(CheckedPointData.id.desc()).first()
        checked_point_data.user_answer = submit
        checked_point_data.status = Status.done.value
        db.session.commit()
        return redirect(url_for('script_runner.run_script', checked_point_id=checked_point_id, path=path))
    return redirect(url_for('index'))


@login_required
@blueprint.route('/show_question/<checked_point_id>')
def show_question(checked_point_id):
    if is_allowed_to_this_work(checked_point_id):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=checked_point_id).order_by(CheckedPointData.id.desc()).first()
        page_content = eval(checked_point_data.page_content)
        message = page_content['message']
        choice = page_content['choice']
        path = page_content['path']
        if current_user.is_authenticated:
            form = ShowQuestionForm(choice)
            return render_template('scripts/show_question.html', message=message, choice=choice,
                                   form=form, checked_point_id=checked_point_id, path=path)
    return redirect(url_for('index'))


@login_required
@blueprint.route('/process-show_question/<choice>-<checked_point_id>-<path>', methods=['POST'])
def processing_show_question(choice, checked_point_id, path):
    if is_allowed_to_this_work(checked_point_id):
        form = ShowQuestionForm(choice)
        choice = str(form.choice.data)
        submit = str(form.submit.data)
        user_answer = str({'choice': choice, 'submit': submit})
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=checked_point_id).order_by(CheckedPointData.id.desc()).first()
        checked_point_data.user_answer = user_answer
        checked_point_data.status = Status.done.value
        db.session.commit()
        return redirect(url_for('script_runner.run_script', checked_point_id=checked_point_id, path=path))
    return redirect(url_for('index'))


@login_required
@blueprint.route('/show_number/<checked_point_id>')
def show_number(checked_point_id):
    if is_allowed_to_this_work(checked_point_id):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=checked_point_id).order_by(CheckedPointData.id.desc()).first()
        page_content = eval(checked_point_data.page_content)
        message = page_content['message']
        path = page_content['path']
        form = ShowNumberForm()
        return render_template('scripts/show_number.html', message=message,
                               form=form, checked_point_id=checked_point_id, path=path)
    return redirect(url_for('index'))


@login_required
@blueprint.route('/process-show_number/<checked_point_id>-<path>', methods=['POST'])
def processing_show_number(checked_point_id, path):
    if is_allowed_to_this_work(checked_point_id):
        form = ShowNumberForm()
        number = str(form.number.data)
        submit = str(form.submit.data)
        user_answer = str({'number': number, 'submit': submit})
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=checked_point_id).order_by(CheckedPointData.id.desc()).first()
        checked_point_data.user_answer = user_answer
        checked_point_data.status = Status.done.value
        db.session.commit()
        return redirect(url_for('script_runner.run_script', checked_point_id=checked_point_id, path=path))
    return redirect(url_for('index'))
