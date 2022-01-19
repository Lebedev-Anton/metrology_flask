from web_app import db
from web_app.user.models import PositionsEmployees, Users
from web_app.admin.models import Devices, AccessRights


def check_employee_position(employee_position):
    positions_from_db = db.session.query(PositionsEmployees.position_name).all()
    allowed_positions = [position[0] for position in positions_from_db]
    message = 'Корректная должнность: должность указана корректна'
    is_valid = True
    if employee_position not in allowed_positions:
        message = 'Некорректная должность: такой должнности не сущестует'
        is_valid = False

    return is_valid, message


def check_commercial_at(user_email):
    return not ('@' in user_email)


def check_domain_name(user_email):
    domain_name = user_email.split('@')[1]
    return not ('.' in domain_name)


def check_spaces_in_mail(user_email):
    return ' ' in user_email


def check_email_correctness(user_email):
    message = 'Корректный email'
    is_valid = True
    if check_commercial_at(user_email):
        message = 'Некорректный email: не указан @'
        is_valid = False
    elif check_domain_name(user_email):
        message = 'Некорректный email: ошибка в домене'
        is_valid = False
    elif check_spaces_in_mail(user_email):
        message = 'Некорректный email: обнаружены лишние пробелы'
        is_valid = False

    return is_valid, message


def check_username(username):
    users_from_db = db.session.query(Users.username).all()
    users = [user[0] for user in users_from_db]
    message = 'Корректное имя пользователя: имя пользователя корректно'
    is_valid = True
    if username in users:
        message = 'Некоректное имя пользователя: такое имя пользователя уже существует'
        is_valid = False

    return is_valid, message


def check_password(password, repeated_password):
    message = 'Корректный пароль: пароль введен корректно'
    is_valid = True
    if len(password) < 8:
        message = 'Не корректный пароль: пароль должен быть не менее 8 символов'
        is_valid = False
    elif password != repeated_password:
        message = 'Не корректный пароль: пароли должены совпадать'
        is_valid = False

    return is_valid, message


def check_employee_admission(order_number, username):
    id_work_type = Devices.query.filter_by(order_number=order_number).first().id_work_type
    access_rights = AccessRights.query.filter_by(id_work_type=id_work_type).all()
    id_allowed_users = [access_right.id_user for access_right in access_rights]
    id_user = Users.query.filter_by(username=username).first().id
    message = 'Не верно выбран пользователь: у выбранного пользователя нет доступа к виду работ'
    is_valid = False
    if id_user in id_allowed_users:
        message = 'Пользователь выбран верно'
        is_valid = True

    return is_valid, message
