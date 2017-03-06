# -*- coding: utf-8 -*-

from flask_peewee.db import Database, ForeignKeyField
from flask_peewee.db import IntegerField, CharField, DateField, FloatField

from app import app

db = Database(app)


class Summary(db.Model):

    date = DateField()
    game = CharField()
    min = IntegerField()
    plays = IntegerField()
    wagered = FloatField()
    winnings = FloatField()
    pending = FloatField()
    identifier = CharField()

    def __repr__(self):
        return "{} | {} | {} | wagered {} | winnings {} | unique_id {}".format(
            self.id, self.date, self.game, self.wagered, self.winnings,
            self.identifier
        )


class Detail(db.Model):

    game_id = CharField()
    time = DateField()
    wagered = FloatField
    result = FloatField()
    summary_id = ForeignKeyField(Summary)
    identifier = CharField()


class Description(db.Model):

    hand = CharField()
    summ = IntegerField()
    cards = CharField()
    action = CharField()
    rate = FloatField()
    win = FloatField()
    detail_id = ForeignKeyField(Detail)
