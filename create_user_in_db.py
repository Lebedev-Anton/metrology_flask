from web_app import db, app
from web_app.user.models import Users, PositionsEmployees


def create_positions(list_positions):
    position_dictionary = [{'position_name': position} for position in list_positions]
    db.session.bulk_insert_mappings(PositionsEmployees, position_dictionary)
    db.session.commit()


def create_user(user_name, position, email, password):
    id_position = PositionsEmployees.query.filter(PositionsEmployees.position_name == position).first().id

    user = Users(user_name=user_name, id_employee_position=id_position, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()


def update_user(username):
    user = Users.query.filter_by(id=23).first()
    user.user_name = username
    db.session.commit()


def get_user_position():
    user = Users.query.filter_by(id=23).first()
    print(user.position.position_name)


positions = ['Начальник лаборатории', 'Начальник сектора', 'Поверитель']

create_positions(positions)

create_user('Вася', 'Начальник лаборатори', 'vasya@mail.ru', '12345678')
create_user('Петя', 'Начальник сектора', 'petya@mail.ru', '12345678')
create_user('Коля', 'Поверитель', 'Kolya@mail.ru', '12345678')
create_user('Иван', 'Поверитель', 'Ivan@mail.ru', '12345678')
