
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

from bljk.app import app, admin


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
    strategy = db.Column(db.Boolean)
    confirmed = db.Column(db.Boolean)
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
    strategy = db.Column(db.Boolean)
    rate = db.Column(db.Float)
    win = db.Column(db.Float)
    detail_id = db.Column(db.Integer)

    def __init__(self, detail_id):
        self.detail_id = detail_id

    def __repr__(self):
        return '<Detail_id {}>'.format(self.detail_id)


class Strategy(db.Model):

    __tablename__ = 'strategy'

    id = db.Column(db.Integer, primary_key=True)
    dealer = db.Column(db.String(4))
    cards = db.Column(db.String(16))
    action = db.Column(db.String(16))

    def __repr__(self):
        return '<{} : {} : {}>'.format(
            self.dealer,
            self.cards,
            self.action,
        )


class SummaryAdmin(ModelView):

    column_list = (
        "date",
        "game",
        "min",
        "plays",
        "wagered",
        "winnings",
        "pending",
        "identifier"
    )
    column_editable_list = column_list
    column_searchable_list = column_list
    column_filters = column_list


class DetailAdmin(ModelView):

    column_list = (
        "game_id",
        "time",
        "wagered",
        "result",
        "summary_id",
        "strategy",
        "confirmed",
        "identifier"
    )
    column_editable_list = column_list
    column_searchable_list = column_list
    column_filters = column_list


class DescriptionlAdmin(ModelView):

    column_list = (
        "hand",
        "summ",
        "cards",
        "action",
        "strategy",
        "rate",
        "win",
        "detail_id"
    )
    column_editable_list = column_list
    column_searchable_list = column_list
    column_filters = column_list


class StrategyAdmin(ModelView):

    column_list = ("dealer", "cards", "action")
    column_editable_list = column_list
    column_searchable_list = column_list
    column_filters = column_list

admin.add_view(StrategyAdmin(Strategy, db.session))
admin.add_view(SummaryAdmin(Summary, db.session))
admin.add_view(DetailAdmin(Detail, db.session))
admin.add_view(DescriptionlAdmin(Description, db.session))
