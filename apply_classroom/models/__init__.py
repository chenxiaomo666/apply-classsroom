from .. import db, app
from .user import User


def init_model():
    db.create_all(app=app)