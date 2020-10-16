from sqlalchemy import or_
from ..models import User
from ..config import Config
from .. import db
import datetime


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
            "is_admin": user.is_admin,
            "openid": user.openid,
            "nickname": user.nickname,
            "head_img": user.head_img,
            "sex": user.sex
        }


