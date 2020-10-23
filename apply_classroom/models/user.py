# coding:utf-8

from .. import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64))
    phone = db.Column("phone", db.String(64))
    student_id = db.Column("student_id", db.Integer)
    register_time = db.Column("register_time", db.DateTime)
    update_time = db.Column("update_time", db.DateTime)
    is_admin = db.Column("is_admin", db.Integer, default=0)    # admin可以审核
    openid = db.Column("openid", db.String(64))
    nickname = db.Column("nickname", db.String(64))
    head_img = db.Column("head_img", db.String(500))
    sex = db.Column("sex", db.Integer)     # 0：女生，1：男生（还有个2，，，应该是未标注性别）
    is_delete = db.Column("is_delete", db.Integer)
