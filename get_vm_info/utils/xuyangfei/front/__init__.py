# -*- coding: utf-8 -*-
import os
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy


BASEDIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATEDIR = os.path.join(BASEDIR, 'templates')
DB_CONNECT_STRING = 'mysql+mysqldb://root:123456@localhost/test'
app = Flask(__name__, template_folder=TEMPLATEDIR)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECT_STRING
app.config['SECRET_KEY'] = 'hard to guess'
db = SQLAlchemy(app)
Base = declarative_base()

