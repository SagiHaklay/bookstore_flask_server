from functools import wraps

from flask import jsonify, abort
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper   

# def user_id_required():
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request()
#             curr_user = get_jwt_identity()
#             if curr_user == str(id):
#                 return fn(*args, **kwargs)
#             else:
#                 return jsonify(msg="Invalid token for user ID!"), 401
#         return decorator
#     return wrapper

def verify_user_id(user_id):
    curr_user = get_jwt_identity()
    if curr_user != str(user_id):
        abort(403, msg='Invalid token for user')