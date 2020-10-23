# coding:utf-8

from .. import db


class ApplyRecord(db.Model):
    __tablename__ = 'apply_record'

    id = db.Column("id", db.Integer, primary_key=True)
    room_id = db.Column("room_id", db.Integer)
    room_name = db.Column("room_name", db.String(64))
    apply_date = db.Column("apply_date", db.DateTime)    # 哪一天
    apply_time = db.Column("apply_time", db.Integer)    # 枚举，1：一二节课，3：三四节课，5：五六节课，7：七八节课，9：九十节课
    apply_status = db.Column("apply_status", db.Integer)    # 枚举，0：未申请，1：申请中（尚未审核通过），2：已申请
    user_id = db.Column("user_id", db.Integer)   # 申请者的user_id
    user_name = db.Column("user_name", db.String(64))
    user_phone = db.Column("user_phone", db.String(64))
    apply_reason = db.Column("apply_reason", db.Text)
    dispose_by = db.Column("dispose_by", db.Integer)    # 处理申请者的user_id，若该字段不为空，且apply_status值为0（未申请），代表是管理员拒绝了该申请
    submit_time = db.Column("submit_time", db.DateTime)   # 学生申请时间
    dispose_time = db.Column("dispose_time", db.DateTime)   # 管理员处理时间
    is_delete = db.Column("is_delete", db.Integer)
