from web_app import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from web_app.admin.models import WorkStatus


class CheckedPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, ForeignKey(WorkStatus.id))
    checked_point_name = db.Column(db.Text)
    checked_point_parameters = db.Column(db.Text)
    status = db.Column(db.Text, default='backlog')

    checked_point_data = relationship("CheckedPointData", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, checked_point_name - {self.checked_point_name}'


class CheckedPointData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_checked_point = db.Column(db.Integer, ForeignKey(CheckedPoint.id))
    current_method = db.Column(db.Text)
    next_method = db.Column(db.Text)
    user_answer = db.Column(db.Text)
    status = db.Column(db.Text, default='backlog')

    def __repr__(self):
        return f'id - {self.id}, current_method - {self.current_method}, next_method - {self.next_method}'