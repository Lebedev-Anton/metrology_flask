from flask import render_template, jsonify
from web_app.forms import SelectScript
from web_app.admin.models import Devices, WorkStatus
from web_app.scripts.models import Scripts
from web_app.script_runner.models import CheckedPoint, CheckedPointData
from flask_login import login_required
from web_app import db
from web_app.script_runner.celery_tasks import start_script_in_celery, run_script_in_celery


from flask import Blueprint

blueprint = Blueprint('script_runner', __name__, url_prefix='/script_runner')


@login_required
@blueprint.route('/start_script', methods=['POST'])
def start_script():
    form = SelectScript()
    if form.validate_on_submit():
        work_id = db.session.query(WorkStatus.id).join(Devices).filter(
            Devices.order_number == form.order_number.data).first()[0]
        script_path_for_import = Scripts.query.filter_by(script_name=form.script.data).first().path
        celery_task = start_script_in_celery.delay(work_id, script_path_for_import)
        title = "Loading..."
        return render_template('scripts/base_script.html', task_id=celery_task.id, title=title)
    return render_template('index.html', form=form)


@login_required
@blueprint.route('/run_script/<checked_point_id>-<path>', methods=['GET', 'POST'])
def run_script(checked_point_id, path):
    work_id = db.session.query(CheckedPoint.id_work).join(CheckedPointData).filter(
        CheckedPointData.id_checked_point == checked_point_id).first()[0]
    celery_task = run_script_in_celery.delay(work_id, path)
    title = "Loading..."
    return render_template('scripts/base_script.html', task_id=celery_task.id, title=title)


@login_required
@blueprint.route('/task_status/<task_id>', methods=['GET', 'POST'])
def task_status(task_id):
    task = start_script_in_celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        return render_template('scripts/base_script.html', task_id=task_id)
    elif task.state != 'FAILURE':
        return task.result
    return str(task.info)


@blueprint.route('/expect_execution_task/<task_id>', methods=['GET', 'POST'])
def expect_execution_task(task_id):
    task = start_script_in_celery.AsyncResult(task_id)
    return jsonify({"state": task.state})
