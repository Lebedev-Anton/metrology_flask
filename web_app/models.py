from web_app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.Text, index=True)
    order_number = db.Column(db.Text, index=True)
    modification = db.Column(db.Text)
    delivery_date = db.Column(db.DateTime)

    work_status = relationship('WorkStatus', lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, serial_number - {self.serial_number}, order_number - {self.order_number}'


class PositionsEmployees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.Text, unique=True)

    users = relationship("Users", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, position_name - {self.position_name}'


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, index=True, unique=True)
    id_employee_position = db.Column(db.Integer, ForeignKey(PositionsEmployees.id))
    email = db.Column(db.Text)
    password_hash = db.Column(db.Text, index=True)

    work_status = relationship("WorkStatus", lazy="joined")
    access_rights = relationship("AccessRights", lazy="joined")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'id - {self.id}, user_name - {self.user_name}, employee_position - {self.employee_position}'


class WorkStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_device = db.Column(db.Integer, db.ForeignKey(Devices.id))
    work_status = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    user_data = relationship("UserData", lazy="joined")
    protocols = relationship("Protocols", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, work_status - {self.work_status}'


class UserData(db.Model):
    """
        Модель для хранения данных, вносимых пользователем в ходе работ
    """
    id = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, db.ForeignKey(WorkStatus.id))
    base_name = db.Column(db.Text)
    path = db.Column(db.Text)

    def __repr__(self):
        return f'id - {self.id}, base_name - {self.base_name}, path - {self.path}'


class Protocols(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, db.ForeignKey(WorkStatus.id))
    protocol_name = db.Column(db.Text)
    path = db.Column(db.Text)

    def __repr__(self):
        return f'id - {self.id}, protocol_name - {self.protocol_name}, path - {self.path}'


class WorkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_type_name = db.Column(db.Text)

    scripts = relationship("Scripts", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, work_type_name - {self.work_type_name}'


class Scripts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wt = db.Column(db.Integer, db.ForeignKey(WorkType.id))
    script_name = db.Column(db.Text)

    access_rights = relationship("AccessRights", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, script_name - {self.script_name}, path - {self.path}'


class AccessRights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id))
    id_script = db.Column(db.Integer, db.ForeignKey(Scripts.id))

    def __repr__(self):
        return f'id - {self.id}, id_user - {self.id_user}, id_script - {self.id_script}'


