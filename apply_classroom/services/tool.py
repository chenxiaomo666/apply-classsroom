from sqlalchemy import or_
from ..models import User, ApplyRecord
from ..config import Config
from .. import db
import datetime

num_han = {1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"日"}
apply_time_han = {1:"一二节课", 3:"三四节课", 5:"五六节课", 7:"七八节课", 9:"九十节课"}


def base_query(model):
    """
    所有未被删除的记录
    """
    return model.query.filter(or_(model.is_delete.is_(None), model.is_delete == 0))


def get_user_info(user_id):

    user = base_query(User).filter_by(id=user_id).first()
    if user is None:
        return {}
    else:
        return {
            "user_id": user.id,
            "name": user.name,
            "phone": user.phone,
            "student_id": user.student_id,
            "register_time": user.register_time,
            "update_time": user.update_time,
            "is_admin": user.is_admin,
            "openid": user.openid,
            "nickname": user.nickname,
            "head_img": user.head_img,
            "sex": user.sex
        }

def get_record_info(record_id):
    record = base_query(ApplyRecord).filter_by(id=record_id).first()
    
    cur = {}
    if record is not None:
        cur["record_id"] = record.id
        cur["room_id"] = record.room_id
        cur["room_name"] = record.room_name
        cur["apply_date"] = str(record.apply_date)[:10]
        cur["weekday"] = num_han[record.apply_date.weekday()+1]
        cur["apply_time"] = apply_time_han[record.apply_time]
        cur["apply_status"] = record.apply_status
        cur["user_id"] = record.user_id
        user_info = get_user_info(record.user_id)
        cur["user_name"] = user_info.get("name")
        cur["user_phone"] = user_info.get("phone")
        cur["apply_reason"] = record.apply_reason
        cur["dispose_by"] = record.dispose_by
        cur["submit_time"] = record.submit_time
        cur["dispose_time"] = record.dispose_time
    
    return cur


def get_student_list():
    users = base_query(User).all()
    result = []
    for user in users:
        result.append(get_user_info(user.id))

    return result

def get_admin_list():
    users = base_query(User).filter_by(is_admin=1).all()
    result = []
    for user in users:
        result.append(get_user_info(user.id))

    return result


# 清除apply_record无用记录
def del_apply_record():
    now = datetime.datetime.now()
    yesterday_now = now - datetime.timedelta(days=1)

    records = base_query(ApplyRecord).filter(ApplyRecord.apply_date<yesterday_now).all()
    for record in records:
        db.session.delete(record)
    
    db.session.commit()

    return None


# add admin
def add_admin(user_id):
    user = base_query(User).filter_by(id=user_id).first()
    
    if user is not None:
        user.is_admin = 1
    
    db.session.commit()

    return None


# change admin to ordinary
def del_admin(user_id):
    user = base_query(User).filter_by(id=user_id).first()
    
    if user is not None:
        user.is_admin = 0
    
    db.session.commit()

    return None
