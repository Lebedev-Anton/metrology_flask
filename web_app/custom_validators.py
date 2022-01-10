from web_app import db
from web_app.user.models import PositionsEmployees, Users


def check_employee_position(employee_position):
    positions_from_db = db.session.query(PositionsEmployees.position_name).all()
    allowed_positions = [position[0] for position in positions_from_db]
    if employee_position in allowed_positions:
        message = 'Корректная должнность: должность указана корректна'
        is_valid = True
    else:
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
    if check_commercial_at(user_email):
        message = 'Некорректный email: не указан @'
        is_valid = False
    elif check_domain_name(user_email):
        message = 'Некорректный email: ошибка в домене'
        is_valid = False
    elif check_spaces_in_mail(user_email):
        message = 'Некорректный email: обнаружены лишние пробелы'
        is_valid = False
    else:
        message = 'Корректный email'
        is_valid = True
    return is_valid, message


def check_username(username):
    users_from_db = db.session.query(Users.username).all()
    users = [user[0] for user in users_from_db]
    if username in users:
        message = 'Некоректное имя пользователя: такое имя пользователя уже существует'
        is_valid = False
    else:
        message = 'Корректное имя пользователя: имя пользователя корректно'
        is_valid = True
    return is_valid, message


def check_password(password, repeated_password):
    if len(password) < 8:
        message = 'Не корректный пароль: пароль должен быть не менее 8 символов'
        is_valid = False
    elif password != repeated_password:
        message = 'Не корректный пароль: пароли должены совпадать'
        is_valid = False
    else:
        message = 'Корректный пароль: пароль введен корректно'
        is_valid = True
    return is_valid, message
