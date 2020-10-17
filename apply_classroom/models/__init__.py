from .. import db, app
from .user import User
from .alternative_room import AlternativeRoom
from .apply_record import ApplyRecord


def init_model():
    db.create_all(app=app)