# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

DATABASE = {
    'name': 'rest.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'

app.config.from_object(__name__)
