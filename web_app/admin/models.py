from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from web_app import db
from web_app.user.models import Users


class WorkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_type_name = db.Column(db.Text)

    scripts = relationship("Scripts", lazy="joined")
    access = relationship("AccessRights", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, work_type_name - {self.work_type_name}'


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.Text, index=True)
    order_number = db.Column(db.Text, index=True)
    modification = db.Column(db.Text)
    delivery_date = db.Column(db.DateTime)
    id_work_type = db.Column(db.Integer, ForeignKey(WorkType.id))

    work_status = relationship('WorkStatus', lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, serial_number - {self.serial_number}, order_number - {self.order_number}'


class WorkStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_device = db.Column(db.Integer, ForeignKey(Devices.id))
    work_status = db.Column(db.Text)
    user_id = db.Column(db.Integer, ForeignKey(Users.id))
    global_data = db.Column(db.Text)

    user_data = relationship("UserData", lazy="joined")
    protocols = relationship("Protocols", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, work_status - {self.work_status}, global_data - {self.global_data}'


class AccessRights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, ForeignKey(Users.id))
    id_work_type = db.Column(db.Integer, ForeignKey(WorkType.id))

    user = relationship('Users', lazy="joined")
    work_type = relationship('WorkType', lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, id_user - {self.id_user}, id_work_type - {self.id_work_type}'
