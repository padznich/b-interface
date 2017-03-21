
# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_admin import Admin
from flask import request
from werkzeug import url_encode


base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    root_path=base_dir,
    # template_folder=os.path.join(base_dir, "templates"),
    # static_path=os.path.join(base_dir, "static"),

)

app.config.from_object('config.LocalConfig')

admin = Admin(app, name='bljk', template_mode='bootstrap3')

@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, url_encode(args))
