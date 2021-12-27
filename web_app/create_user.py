from web_app import app, db
from web_app.models import Users, PositionsEmployees


def create_new_user(username, password, employee_position, email):
    with app.app_context():
        id_position = PositionsEmployees.query.filter(PositionsEmployees.position_name == employee_position).first().id
        new_user = Users(user_name=username, id_employee_position=id_position, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        message = 'Новый пользователь успешно добавлен'
        return True, message
