# coding:utf-8

from .. import db


class AlternativeRoom(db.Model):
    __tablename__ = 'alternative_room'

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64))
    charge = db.Column("charge", db.String(64))
    is_delete = db.Column("is_delete", db.Integer)
