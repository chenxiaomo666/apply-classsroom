# coding:utf-8

from .. import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64))
    is_admin = db.Column("is_admin", db.Integer)    # admin可以审核，并且不用审核直接申请
    openid = db.Column("openid", db.String(64))
    nickname = db.Column("nickname", db.String(64))
    head_img = db.Column("head_img", db.String(500))
    sex = db.Column("sex", db.Integer)     # 0：女生，1：男生
    is_delete = db.Column("is_delete", db.Integer)
