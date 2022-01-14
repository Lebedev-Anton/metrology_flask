from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from web_app.forms import SelectScript
from web_app.models import Scripts, Devices, WorkStatus
from web_app.script_runner.runner import load_checked_point_in_db, run_checked_point
from web_app.script_runner.models import CheckedPoint, CheckedPointData
from web_app import db

from flask import Blueprint

blueprint = Blueprint('script_runner', __name__, url_prefix='/script_runner')


@blueprint.route('/start_script', methods=['POST'])
def start_script():
    form = SelectScript()
    if form.validate_on_submit():
        work_id = db.session.query(WorkStatus.id).join(Devices).filter(
            Devices.order_number == form.order_number.data).first()[0]
        script_path_for_import = Scripts.query.filter_by(script_name=form.script.data).first().path
        load_checked_point_in_db(script_path_for_import, work_id)
        user_id = current_user.id
        return run_checked_point(user_id, work_id, script_path_for_import)
    return render_template('index.html', form=form)


@blueprint.route('/run_script/<checked_point_id>-<path>', methods=['GET', 'POST'])
def run_script(checked_point_id, path):
    work_id = db.session.query(CheckedPoint.id_work).join(CheckedPointData).filter(
        CheckedPointData.id_checked_point == checked_point_id).first()[0]
    user_id = current_user.id
    return run_checked_point(user_id, work_id, path)
