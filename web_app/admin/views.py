from web_app.admin import admin
from web_app import db
from flask_admin.contrib.sqla import ModelView
from web_app.user.models import Users, PositionsEmployees
from web_app.models import AccessRights, WorkType, Devices, WorkStatus
from flask_login import current_user
from web_app.admin.forms import RegistrationForm, EditUserFrom, DevicesForm, WorkStatusForm
from flask import flash
import logging
from flask_admin.babel import gettext

log = logging.getLogger("flask-admin.sqla")


def get_work_types(v, c, m, p):
    id_user = m.id
    work_types_from_db = db.session.query(WorkType.work_type_name). \
        join(AccessRights).filter(AccessRights.id_user == id_user).all()
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
    username = Users.query.filter_by(id=user_id).first().username
    return username


def get_work_status(v, c, m, p):
    id_device = m.id
    try:
        work_status = WorkStatus.query.filter_by(id_device=id_device).first().work_status
    except AttributeError:
        work_status = None
    return work_status


class UserView(ModelView):
    form = RegistrationForm
    column_list = (Users.username, Users.email, 'position.position_name', 'access_rights')
    column_labels = dict(username='Имя пользователя', email='Email')
    column_labels['position.position_name'] = 'Должность сотрудника'
    column_labels['access_rights'] = 'Доступные виды работ'
    column_searchable_list = ('username', 'position.position_name')
    column_sortable_list = ('username', 'email', 'position.position_name')
    create_template = 'admin/create_user.html'
    edit_template = 'admin/edit_user.html'

    column_formatters = dict(access_rights=get_work_types)

    def is_accessible(self):
        return current_user.is_head_of_laboratory

    def create_model(self, form):
        """
             Create model from form.

             :param form:
                 Form instance
         """
        try:
            position_id = PositionsEmployees.query.filter(
                PositionsEmployees.position_name == form.employee_position.data).first().id
            model = Users(username=form.username.data, id_employee_position=position_id, email=form.email.data)
            model.set_password(form.password.data)

            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()

            allowed_work_types = form.allowed_work_types.data
            for work_type in allowed_work_types:
                id_work_type = WorkType.query.filter_by(work_type_name=work_type).first().id
                access_rights = AccessRights(id_user=model.id, id_work_type=id_work_type)
                db.session.add(access_rights)
                db.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def update_model(self, form, model):
        """
            Update model from form.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        try:
            model.username = form.username.data
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            self.session.commit()

            access_rights = AccessRights.query.filter_by(id_user=model.id).all()
            for access_right in access_rights:
                db.session.delete(access_right)
                db.session.commit()

            allowed_work_types = form.allowed_work_types.data
            for work_type in allowed_work_types:
                id_work_type = WorkType.query.filter_by(work_type_name=work_type).first().id
                access_rights = AccessRights(id_user=model.id, id_work_type=id_work_type)
                db.session.add(access_rights)
                db.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to update record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to update record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

        return True

    def get_edit_form(self):
        return EditUserFrom


class DevicesView(ModelView):
    form = DevicesForm
    column_list = (Devices.serial_number, Devices.order_number, Devices.modification, Devices.delivery_date,
                   'work_status.work_status')
    column_labels = dict(serial_number='Серийный номер', order_number='Номер заявки', modification='Модификация',
                         delivery_date='Дата поставки')
    column_labels['work_status.work_status'] = 'Статус работ'

    column_formatters = {'work_status.work_status': get_work_status}

    column_searchable_list = ('serial_number', 'order_number', 'modification', 'delivery_date',
                              'work_status.work_status')
    column_sortable_list = ('serial_number', 'order_number', 'modification', 'delivery_date',
                            'work_status.work_status')

    def is_accessible(self):
        return current_user.is_head_of_laboratory

    def create_model(self, form):
        """
                     Create model from form.

                     :param form:
                         Form instance
                 """
        try:
            id_work_type = WorkType.query.filter_by(work_type_name=form.work_type.data).first().id
            model = Devices(serial_number=form.serial_number.data, order_number=form.order_number.data,
                            modification=form.modification.data, delivery_date=form.delivery_date.data,
                            id_work_type=id_work_type)
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


class WorkStatusView(ModelView):
    column_list = (Devices.order_number, Devices.delivery_date, Users.username)
    column_labels = {'Devices.order_number': 'Номер заявки', 'Devices.delivery_date': 'Дата поставки',
                     'Users.username': 'Имя исполнителя'}

    column_formatters = {'Devices.order_number': get_order_number, 'Devices.delivery_date': get_delivery_date,
                         'Users.username': get_username}
    form = WorkStatusForm

    def is_accessible(self):
        return current_user.is_head_of_laboratory

    def create_model(self, form):
        """
             Create model from form.

             :param form:
                 Form instance
         """
        try:
            id_device = Devices.query.filter_by(order_number=form.order_number.data).first().id
            user_id = Users.query.filter_by(username=form.user.data).first().id
            model = WorkStatus(id_device=id_device, work_status=form.work_status.data, user_id=user_id)
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


admin.add_view(UserView(Users, db.session, category='Настройки пользователей и прав доустпа'))
admin.add_view(DevicesView(Devices, db.session, category='Настройки приборов и статусов работ'))
admin.add_view(WorkStatusView(WorkStatus, db.session, category='Настройки приборов и статусов работ'))
