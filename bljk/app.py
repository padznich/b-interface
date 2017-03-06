# -*- coding: utf-8 -*-

import os

from flask import Flask


base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    root_path=base_dir,
    # template_folder=os.path.join(base_dir, "templates"),
    # static_path=os.path.join(base_dir, "static"),

)
app.config.from_object('config.LocalConfig')
