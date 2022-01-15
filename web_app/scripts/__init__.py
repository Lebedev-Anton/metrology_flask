from web_app import db
from web_app.scripts.forms import ShowMessageForm
from web_app.script_runner.models import CheckedPointData, CheckedPoint
from flask import redirect, url_for
from web_app.forms import SelectScript


class BaseFunction:
    start_method = 'start'

    def __init__(self, checked_point_id, path):
        self.checked_point_id = checked_point_id
        self.path = path

    def show_message(self, message):
        return redirect(url_for('script.show_message', message=message,
                                checked_point_id=self.checked_point_id, path=self.path))

    def show_question(self, message, choice):
        return redirect(url_for('script.show_question', message=message, choice=choice,
                                checked_point_id=self.checked_point_id, path=self.path))

    def show_number(self, message):
        return redirect(url_for('script.show_number', message=message,
                                checked_point_id=self.checked_point_id, path=self.path))

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
        checked_point.status = 'done'

        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=self.checked_point_id).order_by(CheckedPointData.id.desc()).first()
        checked_point_data.status = 'done'
        db.session.commit()
        return redirect(url_for('script_runner.run_script', checked_point_id=self.checked_point_id, path=self.path))

    def redirect_in_next_method(self):
        checked_point_data = CheckedPointData.query.filter_by(
            id_checked_point=self.checked_point_id, current_method='repeat').order_by(
            CheckedPointData.id.desc()).first()
        checked_point_data.status = 'done'
        db.session.commit()
        return redirect(url_for('script_runner.run_script', checked_point_id=self.checked_point_id, path=self.path))

    def get_checked_point_parameters(self):
        checked_point = CheckedPoint.query.filter_by(id=self.checked_point_id).first()
        return checked_point.checked_point_parameters

    def stop_script(self):
        form = SelectScript()
        return redirect(url_for('index', form=form))
