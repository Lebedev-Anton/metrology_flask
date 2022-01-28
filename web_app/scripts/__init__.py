from web_app import db
from web_app.script_runner.models import CheckedPointData, CheckedPoint
from web_app.admin.models import WorkStatus
from flask import redirect, url_for
from web_app.script_runner.enums import Status
from web_app.scripts.models import UserData


class BaseFunction:
    start_method = 'start'

    def __init__(self, checked_point_id, path):
        self.checked_point_id = checked_point_id
        id_work = CheckedPoint.query.filter_by(id=self.checked_point_id).first().id_work
        global_data = WorkStatus.query.filter_by(id=id_work).first().global_data
        if global_data:
            self.global_data = eval(global_data)
        else:
            self.global_data = dict()
        self.path = path

    def show_message(self, message):
        page_content = {'message': message, 'path': self.path}
        self._save_page_content_to_db(page_content)
        return redirect(url_for('script.show_message', checked_point_id=self.checked_point_id))

    def show_question(self, message, choice):
        page_content = {'message': message, 'path': self.path, 'choice': choice}
        self._save_page_content_to_db(page_content)
        return redirect(url_for('script.show_question', checked_point_id=self.checked_point_id))

    def show_number(self, message):
        page_content = {'message': message, 'path': self.path}
        self._save_page_content_to_db(page_content)
        return redirect(url_for('script.show_number', checked_point_id=self.checked_point_id))

    def show_table(self, table_config, message=None):
        page_content = {'table_config': table_config, 'path': self.path, 'message': message}
        self._save_page_content_to_db(page_content)
        return redirect(url_for('script.show_table', checked_point_id=self.checked_point_id))

    def set_global_data(self, parameter_name, value):
        self.global_data.update({parameter_name: value})
        id_work = CheckedPoint.query.filter_by(id=self.checked_point_id).first().id_work
        work_status = WorkStatus.query.filter_by(id=id_work).first()
        work_status.global_data = str(self.global_data)
        db.session.commit()

    def get_global_data(self):
        id_work = CheckedPoint.query.filter_by(id=self.checked_point_id).first().id_work
        work_status = WorkStatus.query.filter_by(id=id_work).first()
        return work_status.global_data

    def return_user_answer(self, method_name):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=self.checked_point_id, current_method=method_name).order_by(
            CheckedPointData.id.desc()).first()
        return checked_point_data.user_answer

    def next_method(self, method):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=self.checked_point_id).order_by(CheckedPointData.id.desc()).first()
        checked_point_data.next_method = method
        db.session.commit()

    def last_method(self):
        checked_point = CheckedPoint.query.filter_by(id=self.checked_point_id).first()
        checked_point.status = Status.done.value

        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=self.checked_point_id).order_by(CheckedPointData.id.desc()).first()
        checked_point_data.status = Status.done.value
        db.session.commit()
        return redirect(url_for('script_runner.run_script', checked_point_id=self.checked_point_id, path=self.path))

    def redirect_in_next_method(self):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=self.checked_point_id, current_method='repeat').order_by(
            CheckedPointData.id.desc()).first()
        checked_point_data.status = Status.done.value
        db.session.commit()
        return redirect(url_for('script_runner.run_script', checked_point_id=self.checked_point_id, path=self.path))

    def get_checked_point_parameters(self):
        checked_point = CheckedPoint.query.filter_by(id=self.checked_point_id).first()
        return checked_point.checked_point_parameters

    def save_protocol_data(self, base_name, data):
        id_work = CheckedPoint.query.filter_by(id=self.checked_point_id).first().id_work
        user_data = UserData(id_work=id_work, base_name=base_name, path=str(data))
        db.session.add(user_data)
        db.session.commit()

    def _save_page_content_to_db(self, page_content_dict):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=self.checked_point_id).order_by(CheckedPointData.id.desc()).first()
        checked_point_data.page_content = str(page_content_dict)
        db.session.commit()
