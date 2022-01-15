import logging
from web_app import db
from web_app.admin.models import WorkType, Devices, WorkStatus, AccessRights
from web_app.user.models import Users
log = logging.getLogger("flask-admin.sqla")


def get_work_types(v, c, m, p):
    id_user = m.id
    work_types_from_db = db.session.query(
        WorkType.work_type_name).join(AccessRights).filter(AccessRights.id_user == id_user).all()
    work_types = []
    for work_type in work_types_from_db:
        work_types.append(str(work_type[0]))
    return work_types


def get_order_number(v, c, m, p):
    id_device = m.id_device
    order_number = Devices.query.filter_by(id=id_device).first().order_number
    return order_number


def get_delivery_date(v, c, m, p):
    id_device = m.id_device
    delivery_date = Devices.query.filter_by(id=id_device).first().delivery_date
    return delivery_date


def get_username(v, c, m, p):
    user_id = m.user_id
    try:
        username = Users.query.filter_by(id=user_id).first().username
    except AttributeError:
        username = None
    return username


def get_work_status(v, c, m, p):
    id_device = m.id
    try:
        work_status = WorkStatus.query.filter_by(id_device=id_device).first().work_status
    except AttributeError:
        work_status = None
    return work_status