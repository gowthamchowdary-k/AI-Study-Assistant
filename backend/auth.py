import os
from functools import wraps
from flask import g

DEFAULT_USER_ID = int(os.getenv("DEFAULT_USER_ID", "1"))


def login_required(f):
    """
    Authentication disabled for the single-user Study Assistant.

    Every request uses the default application user.
    This keeps the existing route structure unchanged.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        g.user_id = DEFAULT_USER_ID
        return f(*args, **kwargs)

    return decorated