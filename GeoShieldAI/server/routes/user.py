"""
User Routes for GeoShield AI
Handles user settings, profile, and account management
"""
from flask import Blueprint, request, jsonify
from routes.auth import token_required
from models.user import User
from database.mongodb import db
import bcrypt
from datetime import datetime

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile information"""
    try:
        user_id = request.user['user_id']
        user = User.get_user_by_id(user_id)
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "profile": {
                "id": str(user['_id']),
                "email": user['email'],
                "name": user.get('name', ''),
                "role": user.get('role', 'officer'),
                "organization": user.get('organization', ''),
                "created_at": user.get('created_at', ''),
                "last_login": user.get('last_login', '')
            }
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/update-profile', methods=['POST'])
@token_required
def update_profile():
    """Update user profile information"""
    try:
        user_id = request.user['user_id']
        data = request.get_json()
        
        update_data = {}
        
        if 'name' in data:
            update_data['name'] = data['name']
        if 'organization' in data:
            update_data['organization'] = data['organization']
        
        if not update_data:
            return jsonify({"success": False, "message": "No data to update"}), 400
        
        result = db.users.update_one(
            {"_id": __import__('bson').ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    """Change user password"""
    try:
        user_id = request.user['user_id']
        data = request.get_json()
        
        if not data.get('currentPassword') or not data.get('newPassword') or not data.get('confirmPassword'):
            return jsonify({"success": False, "message": "All password fields required"}), 400
        
        if data['newPassword'] != data['confirmPassword']:
            return jsonify({"success": False, "message": "Passwords do not match"}), 400
        
        if len(data['newPassword']) < 8:
            return jsonify({"success": False, "message": "Password must be at least 8 characters"}), 400
        
        # Get user
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Verify current password
        if not bcrypt.checkpw(data['currentPassword'].encode('utf-8'), user['password']):
            return jsonify({"success": False, "message": "Current password is incorrect"}), 401
        
        # Hash new password
        hashed_password = bcrypt.hashpw(data['newPassword'].encode('utf-8'), bcrypt.gensalt())
        
        # Update password
        db.users.update_one(
            {"_id": __import__('bson').ObjectId(user_id)},
            {"$set": {"password": hashed_password}}
        )
        
        return jsonify({
            "success": True,
            "message": "Password changed successfully"
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/settings', methods=['GET'])
@token_required
def get_settings():
    """Get user settings"""
    try:
        user_id = request.user['user_id']
        
        # Find or create settings document
        settings = db.user_settings.find_one({"user_id": user_id})
        
        if not settings:
            # Return default settings
            return jsonify({
                "success": True,
                "settings": {
                    "notifications": {
                        "emailAlerts": True,
                        "criticalOnly": False,
                        "dailyDigest": True,
                        "weeklyReport": True,
                        "incidentNotifications": True
                    },
                    "security": {
                        "twoFactorEnabled": False,
                        "sessionTimeout": 30,
                        "ipRestriction": "",
                        "activityLogging": True
                    },
                    "threats": {
                        "minRiskScore": 5,
                        "autoIncidentCreation": True,
                        "threatIntelSources": ["internal", "certin"],
                        "analysisDepth": "standard"
                    }
                }
            }), 200
        
        settings.pop('_id', None)
        
        return jsonify({
            "success": True,
            "settings": settings.get('preferences', {})
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/settings', methods=['POST'])
@token_required
def update_settings():
    """Update user settings"""
    try:
        user_id = request.user['user_id']
        data = request.get_json()
        
        # Prepare settings update
        settings_data = {
            "user_id": user_id,
            "updated_at": datetime.utcnow(),
            "preferences": data
        }
        
        # Save settings (upsert)
        db.user_settings.update_one(
            {"user_id": user_id},
            {"$set": settings_data},
            upsert=True
        )
        
        return jsonify({
            "success": True,
            "message": "Settings updated successfully"
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/activity-log', methods=['GET'])
@token_required
def get_activity_log():
    """Get user activity log"""
    try:
        user_id = request.user['user_id']
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        
        # Get activity logs from database
        activities = list(db.activity_logs.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).skip(skip).limit(limit))
        
        total = db.activity_logs.count_documents({"user_id": user_id})
        
        for activity in activities:
            activity["_id"] = str(activity["_id"])
        
        return jsonify({
            "success": True,
            "activities": activities,
            "total": total,
            "count": len(activities)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/notifications', methods=['GET'])
@token_required
def get_notifications():
    """Get user notifications"""
    try:
        user_id = request.user['user_id']
        limit = int(request.args.get('limit', 20))
        skip = int(request.args.get('skip', 0))
        
        # Get notifications
        notifications = list(db.notifications.find(
            {"user_id": user_id}
        ).sort("created_at", -1).skip(skip).limit(limit))
        
        for notif in notifications:
            notif["_id"] = str(notif["_id"])
        
        unread = db.notifications.count_documents({
            "user_id": user_id,
            "is_read": False
        })
        
        return jsonify({
            "success": True,
            "notifications": notifications,
            "unread": unread,
            "count": len(notifications)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/notifications/<notification_id>/read', methods=['PUT'])
@token_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        db.notifications.update_one(
            {"_id": __import__('bson').ObjectId(notification_id)},
            {"$set": {"is_read": True}}
        )
        
        return jsonify({
            "success": True,
            "message": "Notification marked as read"
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/preferences', methods=['GET'])
@token_required
def get_preferences():
    """Get user preferences"""
    try:
        user_id = request.user['user_id']
        
        prefs = db.user_preferences.find_one({"user_id": user_id})
        
        if not prefs:
            # Return default preferences
            return jsonify({
                "success": True,
                "preferences": {
                    "theme": "dark",
                    "language": "en",
                    "timezone": "IST",
                    "dateFormat": "DD/MM/YYYY"
                }
            }), 200
        
        prefs.pop('_id', None)
        
        return jsonify({
            "success": True,
            "preferences": prefs
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/preferences', methods=['POST'])
@token_required
def update_preferences():
    """Update user preferences"""
    try:
        user_id = request.user['user_id']
        data = request.get_json()
        
        db.user_preferences.update_one(
            {"user_id": user_id},
            {"$set": data},
            upsert=True
        )
        
        return jsonify({
            "success": True,
            "message": "Preferences updated successfully"
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
