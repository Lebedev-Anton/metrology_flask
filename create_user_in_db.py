from web_app import db
from web_app.models import Users, PositionsEmployees


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


positions = ['Начальник лаборатори', 'Начальник сектора', 'Поверитель']

create_positions(positions)

create_user('Вася', 'Начальник лаборатори', 'vasya@mail.ru', '12345678')
create_user('Петя', 'Начальник сектора', 'petya@mail.ru', '12345678')
create_user('Коля', 'Поверитель', 'Kolya@mail.ru', '12345678')
create_user('Иван', 'Поверитель', 'Ivan@mail.ru', '12345678')