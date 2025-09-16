from flask import (
    Blueprint
)
from sqlalchemy import select
from flaskr.database import db
from flaskr.models import User

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def index():
    users = db.session.scalars(select(User).order_by(User.id)).all()
    return [user.to_dict() for user in users]