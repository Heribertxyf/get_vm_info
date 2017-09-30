#!/usr/bin/env python
# -*- coding:utf-8 -*-
from front.homepage_v1 import app
from flask_admin import Admin
from front.__init__ import db
from libs.operate_DB import final
from flask_admin.contrib.sqla import ModelView
if __name__ == "__main__":
    admin = Admin(app)
    admin.add_view(ModelView(final, db.session))
    app.run()
