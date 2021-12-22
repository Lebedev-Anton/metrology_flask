# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from web_app import app
from web_app.create_user import create_new_user
from web_app.forms import SelectScript, EntranceForm, RegistrationForm
from web_app.models import Users

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SelectScript()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/entrance')
def entrance():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Вход"
    entrance_form = EntranceForm()
    return render_template('entrance.html', page_title=title, form=entrance_form)


@app.route('/process-entrance', methods=['POST'])
def process_entrance():
    entrance_form = EntranceForm()
    if entrance_form.validate_on_submit():
        user = Users.query.filter_by(user_name=entrance_form.username.data).first()
        if user and user.check_password(entrance_form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('entrance'))


@app.route('/registration')
def registration():
    title = 'Регистрация'
    registration_form = RegistrationForm()
    return render_template('registration.html', page_title=title, form=registration_form)


@app.route('/process-registration', methods=['POST'])
def registration_entrance():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        result = create_new_user(username=registration_form.username.data, password=registration_form.password.data,
                                 repeated_password=registration_form.repeated_password.data,
                                 employee_position=registration_form.employee_position.data,
                                 email=registration_form.email.data)
        if result.get('status'):
            flash(result.get('message'))
            return redirect(url_for('index'))
        else:
            flash(result.get('message'))
            return redirect(url_for('registration'))
    flash('Проверте правильность заполнения данных')
    return redirect(url_for('registration'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
