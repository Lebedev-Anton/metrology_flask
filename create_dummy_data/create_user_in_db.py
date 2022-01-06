from web_app import db
from web_app.user.models import Users, PositionsEmployees


def save_positions_to_db(positions):
    position_dictionary = [{'position_name': position} for position in positions]
    db.session.bulk_insert_mappings(PositionsEmployees, position_dictionary)
    db.session.commit()


def save_user_to_db(user_name, position, email, password):
    position_id = PositionsEmployees.query.filter(PositionsEmployees.position_name == position).first().id

    user = Users(user_name=user_name, id_employee_position=position_id, email=email)
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

save_positions_to_db(positions)

save_user_to_db('Вася', 'Начальник лаборатори', 'vasya@mail.ru', '12345678')
save_user_to_db('Петя', 'Начальник сектора', 'petya@mail.ru', '12345678')
save_user_to_db('Коля', 'Поверитель', 'Kolya@mail.ru', '12345678')
save_user_to_db('Иван', 'Поверитель', 'Ivan@mail.ru', '12345678')
