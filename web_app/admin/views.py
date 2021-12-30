from web_app.admin import admin
from web_app import db, app
from flask_admin.contrib.sqla import ModelView
from web_app.user.models import Users, PositionsEmployees
from flask_login import current_user
from web_app.admin.forms import RegistrationForm, EditUserFrom
from flask import flash
import logging
from flask_admin.babel import gettext

log = logging.getLogger("flask-admin.sqla")


class UserView(ModelView):
    form = RegistrationForm

    column_list = (Users.user_name, Users.email, 'position.position_name')

    column_labels = dict(user_name='Имя пользователя', email='Email')
    column_labels['position.position_name'] = 'Должность сотрудника'

    column_searchable_list = ('user_name', 'position.position_name')

    column_sortable_list = ('user_name', 'email', 'position.position_name')

    create_template = 'admin/create_user.html'

    edit_template = 'admin/edit_user.html'

    def is_accessible(self):
        return current_user.is_head_of_laboratory

    def create_model(self, form):
        """
             Create model from form.

             :param form:
                 Form instance
         """
        try:
            id_position = PositionsEmployees.query.filter(
                PositionsEmployees.position_name == form.employee_position.data).first().id
            model = Users(user_name=form.username.data, id_employee_position=id_position, email=form.email.data)
            model.set_password(form.password.data)

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

    def update_model(self, form, model):
        """
            Update model from form.

            :param form:
                Form instance
            :param model:
                Model instance
        """
        try:
            model = Users.query.filter_by(id=23).first()
            model.user_name = form.username.data
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            self.session.commit()
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


admin.add_view(UserView(Users, db.session, category='Настройки пользователей и прав доустпа'))
