from flask import Blueprint, request, session
from ..repositorys.props import auth, success, error, panic
from ..models import User, ApplyRecord, AlternativeRoom
from .. import db
from ..config import Config
from ..services.tool import base_query, get_user_info, get_record_info
import requests
import json
import datetime
from sqlalchemy import or_

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
        "open_id": user_openid,
        "user_id": user_id
    })


# 增加用户信息
@user_view.route("/user/upsert", methods=["POST"])
@panic()
def user_upsert():
    data = request.get_json()
    # 如果传过来user_id，不传就是增加
    user_id = data.get("user_id")
    user = base_query(User).filter_by(id=user_id).first()
    if user == None:
        user = User()
        user.name = data["name"]
        user.phone = data["phone"]
        user.student_id = data["student_id"]   # 新增学号字段
        user.register_time = datetime.datetime.now()   # 新增注册时间字段
        user.update_time = datetime.datetime.now()   # 新增更新时间字段
        user.openid = data["openid"]
        user.nickname = data["nickname"]
        user.head_img = data["head_img"]
        user.sex = data["sex"]
        db.session.add(user)
        db.session.flush()
    else:
        user.name = data["name"]
        user.phone = data["phone"]
        user.student_id = data["student_id"]   # 新增学号字段
        user.update_time = datetime.datetime.now()   # 新增更新时间字段 

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


# 查询用户申请教室的历史信息
@user_view.route("/user/record", methods=["GET"])
@panic()
def user_record():

    user_id = request.args.get("user_id")
    user_info = get_user_info(user_id)

    today = datetime.datetime.now()   # 精确到时分秒
    today_date = datetime.datetime(today.year, today.month, today.day)
    
    
    # 个人申请信息是根据实际日期排序的
    # records = base_query(ApplyRecord).filter(ApplyRecord.apply_date>=today_date)
    # .filter_by(user_id=user_id).order_by(ApplyRecord.apply_date.desc()).all()
    records = base_query(ApplyRecord).filter(ApplyRecord.apply_date>=today_date)\
    .filter_by(user_id=user_id).order_by(ApplyRecord.apply_date).all()

    applying = []
    applyed = []
    apply_fail = []
    for record in records:
        if record.apply_status == 1:
            applying.append(get_record_info(record.id))
        elif record.apply_status == 2:
            cur_record = get_record_info(record.id)
            dispose = get_user_info(cur_record["dispose_by"])
            cur_record.update({"dispose_name": dispose["name"]})
            applyed.append(cur_record)
        elif record.apply_status == 0 and record.dispose_by != None:
            cur_record = get_record_info(record.id)
            dispose = get_user_info(cur_record["dispose_by"])
            cur_record.update({"dispose_name": dispose["name"]})
            apply_fail.append(cur_record)

    need_dispose = []   # 所有需要处理的信息
    all_applyed = []    # 所有已申请信息
    if user_info["is_admin"] == 1:
        records = base_query(ApplyRecord).filter(ApplyRecord.apply_date>=today_date).filter_by(apply_status=1).all()
        for record in records:
            need_dispose.append(get_record_info(record.id))

    # 所有已申请信息根据管理员处理时间展示排序
    records = base_query(ApplyRecord).filter(ApplyRecord.apply_date>=today_date)\
    .order_by(ApplyRecord.apply_date.desc()).filter_by(apply_status=2).all()
    for record in records:
        cur_record = get_record_info(record.id)
        dispose = get_user_info(cur_record["dispose_by"])
        cur_record.update({"dispose_name": dispose["name"]})
        all_applyed.append(cur_record)

    option_room_list = []
    rooms = base_query(AlternativeRoom).all()
    for room in rooms:
        cur = {}
        cur["id"] = room.id
        cur["name"] = room.name
        cur["charge"] = room.charge
        option_room_list.append(cur)

    result = {
        "user_info": user_info,
        "applying": applying,
        "applyed": applyed,
        "apply_fail": apply_fail,
        "need_dispose": need_dispose,
        "all_applyed": all_applyed,
        "option_room_list": option_room_list
    }

    return success({
        "result": result
    })


# 根据user的name或者phone查找user
@user_view.route("/user/condition/query", methods=["GET"])
@panic()
def condition_query():
    name = request.args.get("name")
    phone = request.args.get("phone")

    is_find = False
    user_find = {}
    # model.query.filter(or_(model.is_delete.is_(None), model.is_delete == 0))
    user = base_query(User).filter(or_(User.name == name, User.phone == phone)).first()
    if user is not None:
        is_find = True
        user_find = get_user_info(user.id)

    return success({
        "is_find": is_find,
        "user_find": user_find
    })


# 添加管理员
@user_view.route("/admin/add", methods=["POST"])
@panic()
def admin_add():
    data = request.get_json()
    
    is_ok = False
    already_admin = False
    user_id = data["user_id"]
    user = base_query(User).filter_by(id=user_id).first()
    if user is not None:
        if user.is_admin == 0:
            is_ok = True
            user.is_admin = 1
        else:
            is_ok = True
            already_admin = True

    db.session.commit()
    return success({
        "is_ok": is_ok,
        "already_admin": already_admin
    })