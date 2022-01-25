from web_app import db
from web_app.user.models import Users, PositionsEmployees
from web_app.admin.models import WorkType, AccessRights, Devices, WorkStatus
from web_app.scripts.models import Scripts

# Для внесения тестовых данных в базу необходимо выполнить этот скрипт
# Скрипт выполняется только после создания базы


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


def save_work_type_to_db(work_type_name):
    work_type = WorkType(work_type_name=work_type_name)
    db.session.add(work_type)
    db.session.commit()


def save_script_to_db(work_type_name, script_name, path):
    id_wt = WorkType.query.filter_by(work_type_name=work_type_name).first().id
    script = Scripts(id_wt=id_wt, script_name=script_name, path=path)
    db.session.add(script)
    db.session.commit()


def save_access_rights_to_db(user_name, work_type_name):
    user_id = Users.query.filter_by(username=user_name).first().id
    id_wt = WorkType.query.filter_by(work_type_name=work_type_name).first().id
    access_right = AccessRights(id_user=user_id, id_work_type=id_wt)
    db.session.add(access_right)
    db.session.commit()


def save_devices_to_db(serial_number, order_number, modification, delivery_date, work_type_name):
    id_wt = WorkType.query.filter_by(work_type_name=work_type_name).first().id
    device = Devices(serial_number=serial_number, order_number=order_number,
                     modification=modification, delivery_date=delivery_date, id_work_type=id_wt)
    db.session.add(device)
    db.session.commit()


def save_work_status(serial_number, user_name):
    device_id = Devices.query.filter_by(serial_number=serial_number).first().id
    user_id = Users.query.filter_by(username=user_name).first().id
    work_status = WorkStatus(id_device=device_id, work_status='backlog', user_id=user_id)
    db.session.add(work_status)
    db.session.commit()


positions = ['Начальник лаборатории', 'Начальник сектора', 'Поверитель']

save_positions_to_db(positions)

save_user_to_db('Вася', 'Начальник лаборатории', 'vasya@mail.ru', '12345678')
save_user_to_db('Петя', 'Начальник сектора', 'petya@mail.ru', '12345678')
save_user_to_db('Коля', 'Поверитель', 'Kolya@mail.ru', '12345678')
save_user_to_db('Иван', 'Поверитель', 'Ivan@mail.ru', '12345678')

save_work_type_to_db('Поверка алкотестеров')
save_work_type_to_db('Поверка плотномеров')

save_script_to_db('Поверка алкотестеров', 'Динго (49499-12)', 'breathalyzer.dingo_49499_12')
save_script_to_db('Поверка плотномеров', 'ПЛОТ-3 (78813-18)', 'densitometer.plot_3_78813_18')

save_access_rights_to_db('Коля', 'Поверка алкотестеров')
save_access_rights_to_db('Коля', 'Поверка плотномеров')
save_access_rights_to_db('Иван', 'Поверка плотномеров')

save_devices_to_db('test-123', '5A24', 'мод-1', '2022-01-18 00:00:00', 'Поверка алкотестеров')
save_devices_to_db('test-242', '5A25', 'мод-2', '2022-01-18 00:00:00', 'Поверка алкотестеров')
save_devices_to_db('plot-13', '10', 'ПВД', '2022-01-18 00:00:00', 'Поверка плотномеров')

save_work_status('test-123', 'Коля')
save_work_status('test-242', 'Коля')
save_work_status('plot-13', 'Иван')
