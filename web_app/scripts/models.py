from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from web_app import db
from web_app.admin.models import WorkType, WorkStatus


class Scripts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wt = db.Column(db.Integer, db.ForeignKey(WorkType.id))
    script_name = db.Column(db.Text)
    path = db.Column(db.Text)

    work_type = relationship("WorkType", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, script_name - {self.script_name}'


class Protocols(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, db.ForeignKey(WorkStatus.id))
    protocol_name = db.Column(db.Text)
    path = db.Column(db.Text)

    def __repr__(self):
        return f'id - {self.id}, protocol_name - {self.protocol_name}, path - {self.path}'


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, ForeignKey(WorkStatus.id))
    base_name = db.Column(db.Text)
    path = db.Column(db.Text)

    def __repr__(self):
        return f'id - {self.id}, base_name - {self.base_name}, path - {self.path}'