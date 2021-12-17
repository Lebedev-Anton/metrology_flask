# -*- coding: utf-8 -*-
from flask import render_template, url_for, redirect
from web_app import app
from web_app.forms import SelectScript

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SelectScript()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('index.html', form=form)
