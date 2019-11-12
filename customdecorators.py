from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        # user object serialized to JSON
        if get_jwt_identity()['user_level'] != 'admin':
            return {'message':'admin credentials required'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper