from flask import Blueprint, request, session
from ..repositorys.props import auth, success, error, panic
from ..models import User, AlternativeRoom
from .. import db
from ..config import Config
from ..services.tool import base_query, get_user_info
import requests
import json
import datetime

room_view = Blueprint("room_view", __name__)


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
    num_han = {1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"日"}
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
        
