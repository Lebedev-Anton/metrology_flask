from web_app import db


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ser_num = db.Column(db.Text, index=True)
    app_num = db.Column(db.Text, index=True)
    modification = db.Column(db.Text, index=True)
    date = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return f'id - {self.id}, ser_num - {self.ser_num}, app_num - {self.app_num}'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, index=True)
    post = db.Column(db.Text, index=True)
    email = db.Column(db.Text, index=True)
    password_hash = db.Column(db.Text, index=True)

    def __repr__(self):
        return f'id - {self.id}, user_name - {self.user_name}, post - {self.post}'


class WorkStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_device = db.Column(db.Integer, db.ForeignKey(Devices.id))
    work_status = db.Column(db.Text, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __repr__(self):
        return f'id - {self.id}, work_status - {self.work_status}'


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, db.ForeignKey(WorkStatus.id))
    base_name = db.Column(db.Text, index=True)
    path = db.Column(db.Text, index=True)

    def __repr__(self):
        return f'id - {self.id}, base_name - {self.base_name}, path - {self.path}'


class Protocols(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_work = db.Column(db.Integer, db.ForeignKey(WorkStatus.id))
    protocol_name = db.Column(db.Text, index=True)
    path = db.Column(db.Text, index=True)

    def __repr__(self):
        return f'id - {self.id}, protocol_name - {self.protocol_name}, path - {self.path}'


class WorkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_type_name = db.Column(db.Text, index=True)

    def __repr__(self):
        return f'id - {self.id}, work_type_name - {self.work_type_name}'


class Scripts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_wt = db.Column(db.Integer, db.ForeignKey(WorkType.id))
    script_name = db.Column(db.Text, index=True)
    path = db.Column(db.Text, index=True)

    def __repr__(self):
        return f'id - {self.id}, script_name - {self.script_name}, path - {self.path}'


class AccessRigths(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id))
    id_script = db.Column(db.Integer, db.ForeignKey(Scripts.id))

    def __repr__(self):
        return f'id - {self.id}, id_user - {self.id_user}, id_script - {self.id_script}'
