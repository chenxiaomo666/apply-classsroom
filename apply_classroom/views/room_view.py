from flask import Blueprint, request, session
from ..repositorys.props import auth, success, error, panic
from ..models import User, AlternativeRoom, ApplyRecord
from .. import db
from ..config import Config
from ..services.tool import base_query, get_user_info, get_record_info
import requests
import json
import datetime

room_view = Blueprint("room_view", __name__)
num_han = {1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"日"}
apply_time_han = {1:"一二节课", 3:"三四节课", 5:"五六节课", 7:"七八节课", 9:"九十节课"}


# 获取全部可被申请教室的信息
@room_view.route("/alternativeroom/list", methods=["GET"])
@panic()
def alternative_room_list():
    rooms = base_query(AlternativeRoom).all()

    room_list = []
    for room in rooms:
        cur = {}
        cur["id"] = room.id
        cur["name"] = room.name
        room_list.append(cur)

    result = {
        "room_list": room_list
    }

    return success({
        "result": result
    })


# 获取未来十天的日期以及星期几
@room_view.route("/tendate/list", methods=["GET"])
@panic()
def ten_date_list():
    today = datetime.datetime.now()
    date_list = [{
        "date": str(today)[:10],
        "weekday": num_han[today.weekday()+1],
        "delay_day": 0
    }]
    for i in range(1, 10):
        cur_day = today + datetime.timedelta(days=i)
        cur = {}
        cur["date"] = str(cur_day)[:10]
        cur["weekday"] = num_han[cur_day.weekday()+1]
        cur["delay_day"] = i
        date_list.append(cur)

    result = {
        "date_list": date_list
    }

    return success({
        "result": result
    })
        

# 获取一间教室具体某一天的申请情况
@room_view.route("/room/daily", methods=["GET"])
@panic()
def room_daily():

    delay_day = int(request.args.get("delay_day"))
    room_id = request.args.get("room_id")
    room_name = request.args.get("room_name")

    today = datetime.datetime.now()
    query_day = today + datetime.timedelta(days=delay_day)    # 精确到时分秒

    query_date = datetime.datetime(query_day.year, query_day.month, query_day.day)    # 精确到天

    apply_records = base_query(ApplyRecord).filter_by(room_id=room_id, apply_date=query_date).all()
    if apply_records == []:
        for i in range(1, 11, 2):
            apply_record = ApplyRecord()
            apply_record.room_id = room_id
            apply_record.room_name = room_name
            apply_record.apply_date = query_date
            apply_record.apply_time = i
            apply_record.apply_status = 0  # 未申请
            db.session.add(apply_record)
            db.session.flush()
            apply_records.append(apply_record)

    record_list = []
    for record in apply_records:
        cur = get_record_info(record.id)
        record_list.append(cur)

    result = {
        "record_list": record_list,
        "date": str(query_date)[:10],
        "weekday": num_han[query_date.weekday()+1]
    }

    db.session.commit()

    return success({
        "result": result
    })


# 根据record_id获取记录的相关信息
@room_view.route("/record/query", methods=["GET"])
@panic()
def record_query():
    record_id = request.args.get("record_id")
    record = get_record_info(record_id)
    dispose_by = get_user_info(record["dispose_by"])

    return success({
        "record": record,
        "dispose_by": dispose_by,
        "date": record["apply_date"],
        "weekday": record["weekday"]
    })


# 正式申请教室
@room_view.route("/apply/room", methods=["POST"])
@panic()
def apply_room():
    data = request.get_json()

    record_id = data["record_id"]
    apply_user = get_user_info(data["user_id"])
    reason = data["reason"]

    record = base_query(ApplyRecord).filter_by(id=record_id).first()
    if record is None:
        return error(reason="无法根据record_id定位到record")
    else:
        record.apply_status = 1   # 状态更改为申请中
        record.user_id = apply_user["user_id"]
        record.user_name = apply_user["name"]
        record.user_phone = apply_user["phone"]
        record.apply_reason = reason

    db.session.commit()
    return success()


# 管理员同意申请
@room_view.route("/record/agree", methods=["POST"])
@panic()
def record_agree():
    data = request.get_json()

    user_id = data["user_id"]
    record_id = data["record_id"]

    record = base_query(ApplyRecord).filter_by(id=record_id).first()
    record.apply_status = 2
    record.dispose_by = user_id

    db.session.commit()

    return success()


# 管理员同意申请
@room_view.route("/record/disagree", methods=["POST"])
@panic()
def record_disagree():
    data = request.get_json()

    user_id = data["user_id"]
    record_id = data["record_id"]

    record = base_query(ApplyRecord).filter_by(id=record_id).first()
    record.apply_status = 0
    record.dispose_by = user_id

    db.session.commit()

    return success()


# 添加可选择教室
@room_view.route("/room/add", methods=["POST"])
@panic()
def room_add():
    data = request.get_json()
    room_name = data["room_name"]

    is_ok = False
    room = base_query(AlternativeRoom).filter_by(name=room_name).first()
    if room is None:
        is_ok = True
        room = AlternativeRoom()
        room.name = room_name
        db.session.add(room)

    db.session.commit()
    return success({
        "is_ok": is_ok
    })


# 删除教室
@room_view.route("/room/del", methods=["POST"])
@panic()
def room_del():
    data = request.get_json()
    room_id = data["room_id"]

    rooms = base_query(AlternativeRoom).filter_by(id=room_id).all()
    for room in rooms:
        room.is_delete = 1

    records = base_query(ApplyRecord).filter_by(room_id=room_id).all()
    for record in records:
        record.is_delete = 1

    db.session.commit()
    return success()