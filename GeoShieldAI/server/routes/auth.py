"""
Authentication Routes for GeoShield AI
Handles user login, registration, and JWT token management
"""
from flask import Blueprint, request, jsonify
from functools import wraps
from models.user import User
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def token_required(f):
    """Decorator to protect routes with JWT token verification"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"success": False, "message": "Invalid token format"}), 401
        
        if not token:
            return jsonify({"success": False, "message": "Token is missing"}), 401
        
        # Verify token
        payload = User.verify_token(token)
        if not payload:
            return jsonify({"success": False, "message": "Invalid or expired token"}), 401
        
        # Pass user info to the route
        request.user = payload
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user') or request.user.get('role') != 'admin':
            return jsonify({"success": False, "message": "Admin access required"}), 403
        
        return f(*args, **kwargs)
    
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not all(k in data for k in ['email', 'password', 'name']):
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        if len(data['password']) < 6:
            return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400
        
        # Create user
        result = User.create_user(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            role=data.get('role', 'officer')
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validate input
        if not all(k in data for k in ['email', 'password']):
            return jsonify({"success": False, "message": "Missing email or password"}), 400
        
        # Authenticate user
        result = User.authenticate(data['email'], data['password'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user profile"""
    try:
        user = User.get_user_by_id(request.user['user_id'])
        
        if user:
            return jsonify({"success": True, "user": user}), 200
        else:
            return jsonify({"success": False, "message": "User not found"}), 404
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route('/verify-token', methods=['GET'])
@token_required
def verify_token():
    """Verify if token is valid"""
    return jsonify({"success": True, "user": request.user}), 200
