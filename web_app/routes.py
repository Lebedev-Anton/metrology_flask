# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect
from flask_login import current_user
from web_app import app
from web_app.forms import SelectScript


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        title = 'Metrology'
        form = SelectScript()
        return render_template('index.html', title=title, form=form)
    else:
        return redirect(url_for('user.entrance'))
