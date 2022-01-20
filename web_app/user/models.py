from web_app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from web_app.user.enums import EmployeePosition


class PositionsEmployees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.Text, unique=True)

    users = relationship("Users", lazy="joined")

    def __repr__(self):
        return f'id - {self.id}, position_name - {self.position_name}'


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, index=True, unique=True)
    id_employee_position = db.Column(db.Integer, ForeignKey(PositionsEmployees.id))
    email = db.Column(db.Text)
    password_hash = db.Column(db.Text, index=True)

    work_status = relationship("WorkStatus", lazy="joined")
    access_rights = relationship("AccessRights", lazy="joined")
    position = relationship('PositionsEmployees', lazy="joined")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_head_of_laboratory(self):
        id_position = PositionsEmployees.query.filter(
            PositionsEmployees.position_name == EmployeePosition.head_of_laboratory.value).first().id
        return self.id_employee_position == id_position

    @property
    def is_head_of_sector(self):
        id_position = PositionsEmployees.query.filter(
            PositionsEmployees.position_name == EmployeePosition.head_of_sector.value).first().id
        return self.id_employee_position == id_position

    @property
    def is_inspector(self):
        id_position = PositionsEmployees.query.filter(
            PositionsEmployees.position_name == EmployeePosition.verifier.value).first().id
        return self.id_employee_position == id_position

    def __repr__(self):
        return f'id - {self.id}, username - {self.username}, email - {self.email}'
