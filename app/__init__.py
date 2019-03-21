# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, redirect
from app.forms import DataForm
from app.rpn import Rpn
import regex

app = Flask(__name__)
app.config.from_object('config')

rpn = Rpn()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = DataForm()
    #form.result_field.data = rpn.get_status()
    if form.validate_on_submit():
        rpn.clear()
        rpn.push(form.equation_field.data)
        if not rpn.errors:
            form.result_field.data = rpn.get_status()
        else:
            form.errors_field.data = rpn.errors
    return render_template('index.html', 
        title = u'RPN калькулятор',
        form = form)
        