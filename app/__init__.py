# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
from app.forms import DataForm
from app.rpn import Rpn
import time

app = Flask(__name__)
app.config.from_object('config')

rpn = Rpn()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = DataForm()
    execution_time = 0
    if form.validate_on_submit():
        start_time = time.time()
        rpn.clear()
        rpn.push(form.equation_field.data)
        form.result_field.data = rpn.get_status()
        form.errors_field.data = rpn.errors
        execution_time=time.time() - start_time
    return render_template('index.html',
        execution_time = execution_time,
        title = u'RPN калькулятор',
        form = form)
        