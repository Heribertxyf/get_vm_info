# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

now = datetime.now()


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(128))
    address = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return "%s" % self.site_name


class Gpncounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("site.id"))
    source = db.relationship(
        "Site", foreign_keys=[source_id])
    destination_id = db.Column(
        db.Integer, db.ForeignKey("site.id"))
    destination = db.relationship(
        "Site", foreign_keys=[destination_id])
    delay_value = db.Column(db.Integer)
    primary = db.Column(db.Boolean, default=True)
    secondary = db.Column(db.Boolean, default=False)
    update_time = db.Column(db.DateTime, default=now)

    # @classmethod
    # def get_sites(cls):
    # """ 获取所有的节点名称"""
    # sites = cls.query.with_entities(
    # cls.source).group_by(cls.source).all()
    # site_name = [str(site[0]) for site in sites]
    # return site_name

    def __repr__(self):
        return '%s' % self.delay_value
