from web_app import app, db
from web_app.models import Users


def create_new_user(username, password, repeated_password, employee_position, email):
    with app.app_context():
        if Users.query.filter(Users.user_name == username).count():
            return {'status': False, 'message': 'Такой пользователь уже есть'}
        elif not password == repeated_password:
            return {'status': False, 'message': 'Пароли не совпадают'}
        elif check_correctness_of_post(employee_position):
            return {'status': False, 'message': 'Неверно указана должность'}
        elif check_correctness_of_email(email):
            return {'status': False, 'message': 'Не корректный email'}
        else:
            new_user = Users(user_name=username, employee_position=employee_position, email=email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()
            return {'status': True, 'message': 'Новый пользователь успешно добавлен'}


def check_correctness_of_post(user_post):
    # Дописать проверку должности
    return False


def check_correctness_of_email(user_email):
    # Дописать проверку user_email
    return False


if __name__ == '__main__':
    result = create_new_user('Василий Петрович', '12345678', '12345w678', 'Рабочий', 'worker@gmail.com')
    print(result.get('status'), result.get('message'))
