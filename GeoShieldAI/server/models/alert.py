"""
Alert Model for GeoShield AI
Handles security alerts and notifications
"""
from datetime import datetime
from bson.objectid import ObjectId
from database.mongodb import db

class Alert:
    """Alert model for managing security alerts"""
    
    collection = db.alerts
    
    @staticmethod
    def create_alert(alert_data):
        """Create a new alert"""
        try:
            alert_record = {
                "threat_id": alert_data.get("threat_id", ""),
                "title": alert_data.get("title", ""),
                "description": alert_data.get("description", ""),
                "severity": alert_data.get("severity", "medium"),  # low, medium, high, critical
                "category": alert_data.get("category", ""),
                "organization": alert_data.get("organization", ""),
                "district": alert_data.get("district", ""),
                "affected_assets": alert_data.get("affected_assets", []),
                "recommended_action": alert_data.get("recommended_action", ""),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "status": "new",  # new, acknowledged, investigating, resolved
                "acknowledged_by": None,
                "acknowledged_at": None,
                "is_read": False
            }
            
            result = Alert.collection.insert_one(alert_record)
            return {
                "success": True,
                "alert_id": str(result.inserted_id),
                "message": "Alert created successfully"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def get_all_alerts(limit=100, skip=0):
        """Get all alerts with pagination"""
        try:
            alerts = list(Alert.collection.find().sort("created_at", -1).skip(skip).limit(limit))
            for alert in alerts:
                alert["_id"] = str(alert["_id"])
            return alerts
        except Exception as e:
            return []
    
    @staticmethod
    def get_alerts_by_severity(severity):
        """Get alerts by severity level"""
        try:
            alerts = list(Alert.collection.find({"severity": severity}).sort("created_at", -1))
            for alert in alerts:
                alert["_id"] = str(alert["_id"])
            return alerts
        except Exception as e:
            return []
    
    @staticmethod
    def get_unread_alerts():
        """Get all unread alerts"""
        try:
            alerts = list(Alert.collection.find({"is_read": False}).sort("created_at", -1))
            for alert in alerts:
                alert["_id"] = str(alert["_id"])
            return alerts
        except Exception as e:
            return []
    
    @staticmethod
    def mark_as_read(alert_id):
        """Mark alert as read"""
        try:
            result = Alert.collection.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": {"is_read": True, "updated_at": datetime.utcnow()}}
            )
            return {"success": result.modified_count > 0}
        except Exception as e:
            return {"success": False}
    
    @staticmethod
    def acknowledge_alert(alert_id, user_id):
        """Acknowledge an alert"""
        try:
            result = Alert.collection.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": {
                    "status": "acknowledged",
                    "acknowledged_by": user_id,
                    "acknowledged_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }}
            )
            return {"success": result.modified_count > 0}
        except Exception as e:
            return {"success": False}
    
    @staticmethod
    def update_alert_status(alert_id, status):
        """Update alert status"""
        try:
            result = Alert.collection.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": {"status": status, "updated_at": datetime.utcnow()}}
            )
            return {"success": result.modified_count > 0}
        except Exception as e:
            return {"success": False}
