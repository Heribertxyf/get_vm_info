#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from get_vm_info import get_vm_info_app, db

get_vm_info_app.debug = True
manager = Manager(app=get_vm_info_app)

migrate = Migrate(get_vm_info_app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
