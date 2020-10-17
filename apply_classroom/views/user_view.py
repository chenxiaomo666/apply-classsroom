from flask import Blueprint, request, session
from ..repositorys.props import auth, success, error, panic
from ..models import User
from .. import db
from ..config import Config
from ..services.tool import base_query, get_user_info
import requests
import json

user_view = Blueprint("user_view", __name__)


# 查询微信用户是否在本数据库中进行过绑定
@user_view.route("/user/query", methods=["GET"])
@panic()
def user_query():
    data = dict(request.args)

    data.update({
        "appid": Config.APPID,
        "secret": Config.SECRET,
    })

    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = data

    response = requests.get(url=url, params=params)
    user_data = json.loads(response.text)

    user_openid = user_data['openid']


    user = base_query(User).filter_by(openid=user_openid).first()
    if user is not None:
        is_bind = True
        user_id = user.id
    else:
        is_bind = False
        user_id = None

    return success({
        "is_bind": is_bind,
        "user_id": user_id
    })


# 增加用户信息
@user_view.route("/user/upsert", methods=["POST"])
@panic()
def user_upsert():
    data = request.get_json()
    user = User()
    user.name = data["name"]
    user.phone = date["phone"]
    user.openid = data["openid"]
    user.nickname = data["nickname"]
    user.head_img = data["head_img"]
    user.sex = data["sex"]

    db.session.add(user)
    db.session.flush()

    user_id = user.id
    db.session.commit()

    return success({
        "user_id": user_id
    })


# 查询用户信息
@user_view.route("/user/info", methods=["GET"])
@panic()
def user_info():
    user_id = request.args.get("user_id")

    result = get_user_info(user_id)

    return success({
        "result": result
    })