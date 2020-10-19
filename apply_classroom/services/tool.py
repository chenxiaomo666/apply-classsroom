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
        cur["user_name"] = record.user_name
        cur["user_phone"] = record.user_phone
        cur["apply_reason"] = record.apply_reason
        cur["dispose_by"] = record.dispose_by
    
    return cur

