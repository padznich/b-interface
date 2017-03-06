# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask_script import Command

from bljk.models import Summary, Detail, Description, db


class FillDB(Command):

    def __init__(self, _idents=3, _days=60):
        self._idents = _idents
        self._days = _days

    def detail_obj_list(self, summary_id, _ident):

        _dt = Detail(
            summary_id=summary_id
        )

        _dt.identifier = _ident

        for j, row in enumerate(range(20)):
            j += 1
            _dt.game_id = j
            db.session.add(_dt)

    def summary_obj(self, _date, _ident):

        _su = Summary(
            date=_date,
            game="Blackjack Multihand"
        )

        _su.min = 1
        _su.plays = 1
        _su.wagered = 0.1
        _su.winnings = 0.1
        _su.pending = 1
        _su.identifier = _ident

        db.session.add(_su)

    def run(self):

        db.drop_all()
        db.create_all()

        for i in range(1, self._idents + 1):
            for j, _day in enumerate(range(1, self._days)):
                j += 1
                self.summary_obj(datetime.now() - timedelta(days=_day), i)
                self.detail_obj_list(j, i)

        db.session.commit()
