
# -*- coding: utf-8 -*-

import csv

from flask_script import Command

from bljk.models import Strategy, db


STRATEGY_FILE_CSV = "/home/padznich/code/b-interface/strategy.csv"


class FillStrategy(Command):

    def csv_reader(self, path):

        self.strategy = []
        with open(path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.strategy.append(row)

    def fill_strategy(self):

        for row in self.strategy:
            _s = Strategy()
            _s.dealer = row["dealer"]
            _s.cards = row["cards"]
            _s.action = row["action"]

            db.session.add(_s)

    def run(self):

        self.csv_reader(STRATEGY_FILE_CSV)
        self.fill_strategy()

        db.session.commit()
