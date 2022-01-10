from web_app.user.decorators import form_field_validator
from web_app.custom_validators import check_username, check_password, check_email_correctness, check_employee_position
from web_app.models import AccessRights, Devices
from web_app.user.models import Users


@form_field_validator
def validate_username(form, field):
    username = field.data
    check_status, message = check_username(username)
    return check_status, message


@form_field_validator
def validate_password(form, field):
    password = field.data
    repeated_password = form.repeated_password.data
    check_status, message = check_password(password, repeated_password)
    return check_status, message


@form_field_validator
def validate_employee_position(form, field):
    employee_position = field.data
    check_status, message = check_employee_position(employee_position)
    return check_status, message


@form_field_validator
def validate_email(form, field):
    user_email = field.data
    check_status, message = check_email_correctness(user_email)
    return check_status, message


@form_field_validator
def validate_responsible_user(form, field):
    order_number = form.order_number.data
    print(order_number)
    id_work_type = Devices.query.filter_by(order_number=order_number).first().id_work_type
    print(id_work_type)
    access_rights = AccessRights.query.filter_by(id_work_type=id_work_type).all()
    id_allowed_users = [access_right.id_user for access_right in access_rights]
    username = field.data
    id_user = Users.query.filter_by(username=username).first().id
    print(id_user, id_allowed_users)
    if id_user in id_allowed_users:
        message = 'Пользователь выбран верно'
        check_status = True
    else:
        message = 'Не верно выбран пользхователь: у выбранного пользователя нет доступа к виду работ'
        check_status = False

    return check_status, message
