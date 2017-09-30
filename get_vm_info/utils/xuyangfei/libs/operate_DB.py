# -*- coding:utf-8 -*-
from sqlalchemy import Column, INT, VARCHAR
from front.__init__ import Base, DB_CONNECT_STRING, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
'''
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
'''

class TestDB(db.Model):  # 映射到数据表DB
    __tablename__ = 'DB'

    S = db.Column(db.VARCHAR(20), primary_key=True)
    D = db.Column(db.VARCHAR(20))
    weight = db.Column(db.INT)


class final(db.Model):  # 映射到数据表NEW
    __tablename__ = 'NEW'
    Id = db.Column(db.INT, primary_key=True)
    Source = db.Column(db.VARCHAR(20))
    Destination = db.Column(db.VARCHAR(20))
    Weight = db.Column(db.INT)

class Final(db.Model):
    Id = db.Column(db.INT, primary_key=True)
    Source = db.Column(db.VARCHAR(20))
    Destination = db.Column(db.VARCHAR(20))
    Weight = db.Column(db.INT)

    def __init__(self, Source, Destination):
        self.Source = Source
        self.Destination = Destination
db.create_all()


