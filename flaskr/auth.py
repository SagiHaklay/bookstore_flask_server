from flask import (
    Blueprint, jsonify, request, abort
)
from sqlalchemy import select
from flaskr.database import db
from flaskr.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('POST',))
def register():
    if request.is_json:
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    if not username:
        abort(400, description='username required')
    if not password:
        abort(400, description='password required')
    if not email:
        abort(400, description='email required')
    user = User(username=username, password=password, email=email, isAdmin=False)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        abort(500, description='DB insertion error')
    return jsonify(user)

@bp.route('/login', methods=('POST',))
def login():
    # print(request.content_type)
    # print(request.data)
    # print(request.get_json())
    try:
        if request.is_json:
            data = request.get_json()
            username = data['username']
            password = data['password']
        else:
            username = request.form['username']
            password = request.form['password']
    except (KeyError, UnicodeDecodeError) as e:
        print(e)
        abort(400, description='Invalid request data')
    if not username:
        abort(400, description='username required')
    if not password:
        abort(400, description='password required')
    user = db.session.scalar(select(User).where(User.username == username))
    if not user:
        abort(401, description='Username does not exist')
    if user.password != password:
        abort(401, description='Username and/or password are incorrect')
    return {
        'userId': user.id,
        'isAdmin': user.isAdmin,
        'token': 'token'
    }