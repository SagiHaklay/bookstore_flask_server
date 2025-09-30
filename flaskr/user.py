from flask import (
    Blueprint, jsonify, request, abort
)
from sqlalchemy import select
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash
from flaskr.database import db
from flaskr.models import User, UserResponse
from flaskr.validation import verify_user_id

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def index():
    users = db.session.scalars(select(User).order_by(User.id)).all()
    # return [user.to_dict() for user in users]
    return jsonify(users)

@bp.route('/<int:id>', methods=('GET', 'POST'))
@jwt_required()
def get_user(id):
    verify_user_id(id)
    user = db.get_or_404(User, id)
    res = UserResponse(user.id, user.username, user.password, user.email, user.isAdmin)
    return jsonify(res)

@bp.route('/<int:id>/update', methods=('PUT', 'PATCH'))
@jwt_required()
def update(id):
    verify_user_id(id)
    if request.is_json:
        data = request.get_json()
        username = data['username'] if 'username' in data else None
        password = data['password'] if 'password' in data else None
        email = data['email'] if 'email' in data else None
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
    user = db.get_or_404(User, id)
    try:
        if username:
            user.username = username
        if password:
            user.password = generate_password_hash(password)
        if email:
            user.email = email
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500, description='DB update error')
    res = UserResponse(user.id, user.username, user.password, user.email, user.isAdmin)
    return jsonify(res)

@bp.route('/<int:id>/delete', methods=('DELETE',))
@jwt_required()
def remove(id):
    verify_user_id(id)
    user = db.get_or_404(User, id)
    res = UserResponse(user.id, user.username, user.password, user.email, user.isAdmin)
    user_json = jsonify(res)
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500, description='DB delete error')
    return user_json