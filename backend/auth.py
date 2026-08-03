import datetime
import os
from functools import wraps
import jwt
from flask import request, jsonify, g

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "study-assistant-super-jwt-secret-key-2026")

def generate_token(user_id: int) -> str:
    """
    Generates a JWT token for the given user_id, valid for 7 days.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def login_required(f):
    """
    Decorator to protect Flask routes with JWT.
    Expects Bearer <token> in the Authorization header.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            print("AUTH ERROR: Token is missing.")
            return jsonify({
                "success": False,
                "error": "Access denied. Authentication token is missing."
            }), 401
        
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            g.user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            print("AUTH ERROR: Token has expired.")
            return jsonify({
                "success": False,
                "error": "Authentication token has expired. Please login again."
            }), 401
        except jwt.InvalidTokenError as e:
            print(f"AUTH ERROR: Invalid token. Details: {e}")
            return jsonify({
                "success": False,
                "error": "Authentication token is invalid."
            }), 401
        except Exception as e:
            print(f"AUTH ERROR: Unknown exception. Details: {e}")
            return jsonify({
                "success": False,
                "error": "Authentication failed."
            }), 401
            
        return f(*args, **kwargs)
    return decorated
