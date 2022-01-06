from wtforms.validators import ValidationError


def form_field_validator(func_to_validate):
    def validate_func(form, field):
        check_status, message = func_to_validate(form, field)
        if not check_status:
            raise ValidationError(message)
    return validate_func
