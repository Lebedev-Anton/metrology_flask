from flask_login import current_user
from web_app.script_runner.models import CheckedPoint
from web_app.admin.models import WorkStatus


def is_allowed_to_this_work(checked_point_id):
    work_id = CheckedPoint.query.filter_by(id=checked_point_id).first().id_work
    user_id = WorkStatus.query.filter_by(id=work_id).first().user_id
    return current_user.id == user_id
