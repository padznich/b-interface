# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

from bljk.app import app

db = SQLAlchemy(app)


class Summary(db.Model):

    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    game = db.Column(db.String(40))
    min = db.Column(db.Integer)
    plays = db.Column(db.Integer)
    wagered = db.Column(db.Float)
    winnings = db.Column(db.Float)
    pending = db.Column(db.Float)
    identifier = db.Column(db.String(32))

    def __init__(self, date, game):
        self.date = date
        self.game = game

    def __repr__(self):
        return '<date {} game {}>'.format(self.date, self.game)


class Detail(db.Model):

    __tablename__ = 'detail'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(40))
    time = db.Column(db.Date)
    wagered = db.Column(db.Float)
    result = db.Column(db.Float)
    summary_id = db.Column(db.Integer)
    identifier = db.Column(db.String(32))

    def __init__(self, summary_id):
        self.summary_id = summary_id

    def __repr__(self):
        return '<Summary_id {}>'.format(self.summary_id)


class Description(db.Model):

    __tablename__ = 'detail_description'

    id = db.Column(db.Integer, primary_key=True)
    hand = db.Column(db.String(32))
    summ = db.Column(db.Integer)
    cards = db.Column(db.String(32))
    action = db.Column(db.String(32))
    rate = db.Column(db.Float)
    win = db.Column(db.Float)
    detail_id = db.Column(db.Integer)

    def __init__(self, detail_id):
        self.detail_id = detail_id

    def __repr__(self):
        return '<Detail_id {}>'.format(self.detail_id)
