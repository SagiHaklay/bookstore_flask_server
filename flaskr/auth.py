from flask import (
    Blueprint, jsonify, request, abort
)
from sqlalchemy import select
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.database import db
from flaskr.models import User, UserResponse

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
    password = generate_password_hash(password)
    user = User(username=username, password=password, email=email, isAdmin=False)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500, description='DB insertion error')
    res = UserResponse(user.id, user.username, user.password, user.email, user.isAdmin)
    return jsonify(res)

@bp.route('/login', methods=('POST',))
def login():
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
        # abort(401, description='Username does not exist')
        return {'message': 'Username does not exist'}, 401
    if user.password != password and not check_password_hash(user.password, password):
        # abort(401, description='Username and/or password are incorrect')
        return {'message': 'Username and/or password are incorrect'}, 401
    token = create_access_token(identity=str(user.id), additional_claims={'is_admin': user.isAdmin})
    return {
        'userId': user.id,
        'isAdmin': user.isAdmin,
        'token': token
    }
