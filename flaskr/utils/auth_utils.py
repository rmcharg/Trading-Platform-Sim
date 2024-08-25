# Functions used for user authentication
from flask import redirect, session
from functools import wraps

# Decorator for routes so that is login is required
def login_required(orig_func):
    # use wraps so that the decorated function still has the route name
    @wraps(orig_func)
    def decorated_function(*args, **kwargs):
        print(session)
        if session.get("user_id") is None:
            return redirect("/login")
        return orig_func(*args, **kwargs)
    
    return decorated_function