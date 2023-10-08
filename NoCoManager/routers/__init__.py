from functools import wraps
from flask import abort

SERVICES: dict = {
    "ticketer": {"enabled": True, "path": "ticket.index", "title": "Ticketer"},
    "cashless": {
        "enabled": False,
        "path": "cashless.index",
        "title": "CashLess",
    },
}


def isEnabled(is_enabled):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_enabled:
                abort(404)  # Return a 404 Not Found error if routes are disabled
            return f(*args, **kwargs)

        return decorated_function

    return decorator


from .admin import default_bp
from .ticketer import ticket_router
