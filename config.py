# -*- coding: utf-8 -*-


class LocalConfig(object):

    SQLALCHEMY_DATABASE_URI = "sqlite:///../bljk.db"
    SECRET_KEY = "random string"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
