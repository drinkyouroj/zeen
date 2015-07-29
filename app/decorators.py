from functools import wraps
from flask import abort
from flask.ext.login import current_user

def permission_required(permission):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return function(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(function):
    return permission_required(Permission.ADMINISTER)(function)

