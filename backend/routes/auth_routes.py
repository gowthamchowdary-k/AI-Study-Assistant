from flask import Blueprint, request, jsonify, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection
from auth import generate_token, login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user with email and password.
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "Request body must be JSON."
        }), 400
        
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    
    if not email or not password:
        return jsonify({
            "success": False,
            "error": "Email and password are required."
        }), 400
        
    if len(password) < 6:
        return jsonify({
            "success": False,
            "error": "Password must be at least 6 characters long."
        }), 400

    password_hash = generate_password_hash(password)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        token = generate_token(user_id)
        
        return jsonify({
            "success": True,
            "message": "User registered successfully.",
            "token": token,
            "user": {
                "id": user_id,
                "email": email
            }
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "error": "A user with this email already exists."
        }), 400
    except Exception as e:
        print(f"REGISTER ERROR: {e}")
        return jsonify({
            "success": False,
            "error": "An internal error occurred during registration."
        }), 500
    finally:
        conn.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates an existing user and returns a JWT token.
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "Request body must be JSON."
        }), 400
        
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    
    if not email or not password:
        return jsonify({
            "success": False,
            "error": "Email and password are required."
        }), 400
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password_hash FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({
            "success": False,
            "error": "Invalid email or password."
        }), 401
        
    token = generate_token(user["id"])
    
    return jsonify({
        "success": True,
        "message": "Login successful.",
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"]
        }
    })

@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    """
    Returns the current authenticated user details.
    """
    user_id = g.user_id
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({
            "success": False,
            "error": "User not found."
        }), 404
        
    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
    })
