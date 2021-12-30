from web_app.user.decorators import validator
from web_app.custom_validators import check_username, check_password, check_email_correctness, check_employee_position


@validator
def validate_username(form, field):
    username = field.data
    check_status, message = check_username(username)
    return check_status, message


@validator
def validate_password(form, field):
    password = field.data
    repeated_password = form.repeated_password.data
    check_status, message = check_password(password, repeated_password)
    return check_status, message


@validator
def validate_employee_position(form, field):
    employee_position = field.data
    check_status, message = check_employee_position(employee_position)
    return check_status, message


@validator
def validate_email(form, field):
    user_email = field.data
    check_status, message = check_email_correctness(user_email)
    return check_status, message