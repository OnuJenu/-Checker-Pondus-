from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from app.models.user import User
from app import db
import jwt
from app.config import settings
from datetime import datetime

class AuthorizationHeaderMissing(Exception):
    """Raised when Authorization header is missing or invalid"""
    pass

class JWTTokenExpired(Exception):
    """Raised when JWT token is expired"""
    pass

class JWTDecodingError(Exception):
    """Raised when JWT decoding fails"""
    pass

# Error handler mapping
ERROR_HANDLERS = {
    AuthorizationHeaderMissing: (lambda e: ({"error": str(e)}, 401)),
    JWTTokenExpired: (lambda e: ({"error": str(e)}, 401)),
    JWTDecodingError: (lambda e: ({"error": str(e)}, 401)),
}

def handle_auth_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except tuple(ERROR_HANDLERS.keys()) as e:
            handler = ERROR_HANDLERS[type(e)]
            error_response, status_code = handler(e)
            return jsonify(error_response), status_code
    return wrapper

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)

def get_current_user():
    """
    Retrieves the currently logged-in user based on the JWT token.

    Raises:
        AuthorizationHeaderMissing: If Authorization header is missing or invalid
        JWTTokenExpired: If JWT token is expired
        JWTDecodingError: If JWT decoding fails

    Returns:
        User: The current user object
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthorizationHeaderMissing("Authorization header is missing or invalid")
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
            raise JWTTokenExpired("JWT token is expired")
            
        return db.query(User).filter_by(id=payload['user_id']).first()
    except jwt.PyJWTError:
        raise JWTDecodingError("JWT decoding failed")
