from web_app import db
from web_app.user.models import Users, PositionsEmployees
from web_app.models import Scripts, AccessRights, WorkType


def save_positions_to_db(positions):
    position_dictionary = [{'position_name': position} for position in positions]
    db.session.bulk_insert_mappings(PositionsEmployees, position_dictionary)
    db.session.commit()


def save_user_to_db(user_name, position, email, password):
    position_id = PositionsEmployees.query.filter(PositionsEmployees.position_name == position).first().id

    user = Users(username=user_name, id_employee_position=position_id, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()


def update_user(username):
    user = Users.query.filter_by(id=23).first()
    user.username = username
    db.session.commit()


def get_user_position():
    user = Users.query.filter_by(id=23).first()


def get_work_types(model):
    id_user = model.id
    work_types_from_db = db.session.query(WorkType.work_type_name).\
        join(AccessRights).filter(AccessRights.id_user == id_user).all()
    work_types = []
    for work_type in work_types_from_db:
        work_types.append(str(work_type[0]))


if __name__ == '__main__':
    # positions = ['Начальник лаборатории', 'Начальник сектора', 'Поверитель']
    #
    # save_positions_to_db(positions)
    #
    # save_user_to_db('Вася', 'Начальник лаборатори', 'vasya@mail.ru', '12345678')
    # save_user_to_db('Петя', 'Начальник сектора', 'petya@mail.ru', '12345678')
    # save_user_to_db('Коля', 'Поверитель', 'Kolya@mail.ru', '12345678')
    # save_user_to_db('Иван', 'Поверитель', 'Ivan@mail.ru', '12345678')
    # from web_app.models import WorkStatus, Devices
    #
    # work_types = WorkStatus.query(WorkStatus.work_status).filter_by(user_id=26).all()
    # work_types = db.session.query(Devices.order_number).join(WorkStatus).filter(WorkStatus.user_id == 26).all()
    # for work_type in work_types:
    #     print(work_type)
    print(dict({'choise': 'Нет', 'submit': 'True'}))
