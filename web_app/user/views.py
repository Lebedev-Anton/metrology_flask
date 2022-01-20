from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from web_app.user.create_user import create_new_user
from web_app.user.forms import EntranceForm, RegistrationForm
from web_app.user.models import Users

from flask import Blueprint
blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/entrance')
def entrance():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Вход"
    entrance_form = EntranceForm()
    return render_template('user/entrance.html', title=title, form=entrance_form)


@blueprint.route('/process-entrance', methods=['POST'])
def process_entrance():
    entrance_form = EntranceForm()
    if entrance_form.validate_on_submit():
        user = Users.query.filter_by(username=entrance_form.username.data).first()
        if user and user.check_password(entrance_form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.entrance'))


@blueprint.route('/registration')
def registration():
    title = 'Регистрация'
    registration_form = RegistrationForm()
    return render_template('user/registration.html', title=title, form=registration_form)


@blueprint.route('/process-registration', methods=['POST'])
def process_registration():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        check_status, message = create_new_user(username=registration_form.username.data,
                                                password=registration_form.password.data,
                                                employee_position=registration_form.employee_position.data,
                                                email=registration_form.email.data)
        flash(message)
        return redirect(url_for('user.entrance'))
    messages = [registration_form.errors[key][0] for key in registration_form.errors]
    for message in messages:
        flash(message)
    return redirect(url_for('user.registration'))


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
