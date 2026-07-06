"""
User Model for GeoShield AI
Handles user authentication and authorization
"""
from datetime import datetime
from bson.objectid import ObjectId
from database.mongodb import db
import hashlib
import jwt
import os

class User:
    """User model for authentication and authorization"""
    
    collection = db.users
    
    @staticmethod
    def create_user(email, password, name, role="officer"):
        """Create a new user"""
        try:
            # Check if user exists
            if User.collection.find_one({"email": email}):
                return {"success": False, "message": "User already exists"}
            
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            user_data = {
                "email": email,
                "name": name,
                "password_hash": password_hash,
                "role": role,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_active": True
            }
            
            result = User.collection.insert_one(user_data)
            return {
                "success": True,
                "user_id": str(result.inserted_id),
                "message": "User created successfully"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate user with email and password"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            user = User.collection.find_one({
                "email": email,
                "password_hash": password_hash,
                "is_active": True
            })
            
            if not user:
                return {"success": False, "message": "Invalid credentials"}
            
            # Generate JWT token
            token = jwt.encode({
                "user_id": str(user["_id"]),
                "email": user["email"],
                "role": user["role"],
                "exp": datetime.utcnow().timestamp() + 86400 * 7  # 7 days
            }, os.getenv("SECRET_KEY"), algorithm="HS256")
            
            return {
                "success": True,
                "token": token,
                "user": {
                    "id": str(user["_id"]),
                    "email": user["email"],
                    "name": user["name"],
                    "role": user["role"]
                }
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        try:
            user = User.collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return None
            
            del user["password_hash"]
            user["_id"] = str(user["_id"])
            return user
        except Exception as e:
            return None
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            return payload
        except Exception as e:
            return None
