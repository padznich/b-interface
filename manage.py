# -*- coding: utf-8 -*-

from flask_migrate import Manager, Migrate, MigrateCommand

from bljk.models import db
from bljk.views import app
from bljk.management.commands.generate_db_data import FillDB
from bljk.management.commands.generate_strategy import FillStrategy


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('fill_db', FillDB())
manager.add_command('fill_strategy', FillStrategy())


if __name__ == '__main__':
    manager.run()
