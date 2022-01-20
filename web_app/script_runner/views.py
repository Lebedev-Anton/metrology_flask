from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from web_app.forms import SelectScript
from web_app.admin.models import Devices, WorkStatus
from web_app.scripts.models import Scripts
from web_app.script_runner.runner import load_checked_point_in_db, run_checked_point
from web_app.script_runner.models import CheckedPoint, CheckedPointData
from web_app import db, celery_app, app

from flask import Blueprint

blueprint = Blueprint('script_runner', __name__, url_prefix='/script_runner')


@blueprint.route('/start_script', methods=['POST'])
def start_script():
    form = SelectScript()
    if form.validate_on_submit():
        work_id = db.session.query(WorkStatus.id).join(Devices).filter(
            Devices.order_number == form.order_number.data).first()[0]
        script_path_for_import = Scripts.query.filter_by(script_name=form.script.data).first().path
        user_id = current_user.id
        celery_task = run_checked_point_in_celery.delay(work_id, script_path_for_import, user_id)
        return redirect(url_for('script_runner.task_status', task_id=celery_task.id))
    return render_template('index.html', form=form)


@blueprint.route('/run_script/<checked_point_id>-<path>', methods=['GET', 'POST'])
def run_script(checked_point_id, path):
    work_id = db.session.query(CheckedPoint.id_work).join(CheckedPointData).filter(
        CheckedPointData.id_checked_point == checked_point_id).first()[0]
    user_id = current_user.id
    return run_checked_point(user_id, work_id, path)


@blueprint.route('/task_status/<task_id>', methods=['GET', 'POST'])
def task_status(task_id):
    task = run_checked_point_in_celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        return "Задача выполняется. Ожидайте"
    elif task.state != 'FAILURE':
        return task.result
    return str(task.info) + 'ОШИБКА ' + task.state


@celery_app.task(serializer='json')
def run_checked_point_in_celery(work_id, script_path_for_import, user_id):
    with app.app_context(), app.test_request_context():
        load_checked_point_in_db(script_path_for_import, work_id)
        return run_checked_point(user_id, work_id, script_path_for_import)