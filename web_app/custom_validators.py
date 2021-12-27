from web_app import db
from web_app.models import PositionsEmployees, Users


def check_employee_position(employee_position):
    positions_from_db = db.session.query(PositionsEmployees.position_name).all()
    allowed_positions = [position[0] for position in positions_from_db]
    if employee_position in allowed_positions:
        message = 'Корректная должнность: должность указана корректна'
        return True, message
    else:
        message = 'Некорректная должность: такой должнности не сущестует'
        return False, message


def check_email_correctness(user_email):
    def check_commercial_at():
        return not ('@' in user_email)

    def check_domain_name():
        domain_name = user_email.split('@')[1]
        return not ('.' in domain_name)

    def check_spaces_in_mail():
        return ' ' in user_email

    if check_commercial_at():
        message = 'Некорректный email: не указан @'
        return False, message
    elif check_domain_name():
        message = 'Некорректный email: ошибка в домене'
        return False, message
    elif check_spaces_in_mail():
        message = 'Некорректный email: обнаружены лишние пробелы'
        return False, message
    else:
        message = 'Корректный email'
        return True, message


def check_username(username):
    users_from_db = db.session.query(Users.user_name).all()
    users = [user[0] for user in users_from_db]
    if username in users:
        message = 'Некоректное имя пользователя: такое имя пользователя уже существует'
        return False, message
    else:
        message = 'Корректное имя пользователя: имя пользователя корректно'
        return True, message


def check_password(password, repeated_password):
    if len(password) < 8:
        message = 'Не корректный пароль: пароль должен быть не менее 8 символов'
        return False, message
    elif password != repeated_password:
        message = 'Не корректный пароль: пароли должены совпадать'
        return False, message
    else:
        message = 'Корректный пароль: пароль введен корректно'
        return True, message
