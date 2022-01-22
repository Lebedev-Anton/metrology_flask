from web_app import db
from web_app.script_runner.models import CheckedPointData, CheckedPoint
from flask import redirect, url_for
from web_app.forms import SelectScript
from web_app.script_runner.enums import Status


class BaseFunction:
    start_method = 'start'

    def __init__(self, checked_point_id, path):
        self.checked_point_id = checked_point_id
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

    def _save_page_content_to_db(self, page_content_dict):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=self.checked_point_id).order_by(CheckedPointData.id.desc()).first()
        checked_point_data.page_content = str(page_content_dict)
        db.session.commit()
