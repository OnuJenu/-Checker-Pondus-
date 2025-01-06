from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from app.models.user import User

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)

def get_current_user():
    """
    Retrieves the currently logged-in user based on the session data.

    Returns:
        User: The current user object, or None if no user is logged in.
    """
    user_id = session.get('user_id')
    if not user_id:
        return None

    return User.query.get(user_id)
