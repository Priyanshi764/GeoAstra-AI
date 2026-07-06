"""
Geofence Alert Model for GeoShield AI
Manages intelligence-based geofence alerts
"""
from datetime import datetime
from bson.objectid import ObjectId
from database.mongodb import db

class GeofenceAlert:
    """Model for managing cyber geofence alerts"""
    
    collection = db.geofence_alerts
    
    @staticmethod
    def create_alert(alert_data):
        """Create a new geofence alert"""
        try:
            alert_record = {
                "threat_id": alert_data.get("threat_id", ""),
                "title": alert_data.get("title", "Cyber Geofence Triggered"),
                "description": alert_data.get("description", ""),
                "severity": alert_data.get("severity", "medium"),  # low, medium, high, critical
                "risk_score": alert_data.get("risk_score", 50),     # 0-100
                "confidence": alert_data.get("confidence", 50),     # 0-100
                "zone": alert_data.get("zone", "Unknown Zone"),
                "district": alert_data.get("district", "Unknown"),
                "affected_assets": alert_data.get("affected_assets", []),  # List of asset dicts or IDs
                "recommended_actions": alert_data.get("recommended_actions", []),  # List of recommended actions
                "status": alert_data.get("status", "new"),  # new, acknowledged, investigating, resolved
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_read": False,
                "acknowledged_by": None,
                "acknowledged_at": None
            }
            
            result = GeofenceAlert.collection.insert_one(alert_record)
            return {
                "success": True,
                "alert_id": str(result.inserted_id),
                "message": "Geofence alert created successfully"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
            
    @staticmethod
    def get_all_alerts(limit=100, skip=0, query=None):
        """Get all geofence alerts with pagination and filters"""
        try:
            search_query = query if query else {}
            alerts = list(GeofenceAlert.collection.find(search_query).sort("created_at", -1).skip(skip).limit(limit))
            for alert in alerts:
                alert["_id"] = str(alert["_id"])
            return alerts
        except Exception as e:
            return []
            
    @staticmethod
    def get_alert_by_id(alert_id):
        """Get a specific geofence alert by ID"""
        try:
            alert = GeofenceAlert.collection.find_one({"_id": ObjectId(alert_id)})
            if alert:
                alert["_id"] = str(alert["_id"])
            return alert
        except Exception as e:
            return None
            
    @staticmethod
    def update_alert_status(alert_id, status, user_id=None):
        """Update the status of a geofence alert"""
        try:
            update_fields = {
                "status": status,
                "updated_at": datetime.utcnow()
            }
            if status == "acknowledged" and user_id:
                update_fields["acknowledged_by"] = user_id
                update_fields["acknowledged_at"] = datetime.utcnow()
                
            result = GeofenceAlert.collection.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": update_fields}
            )
            return {"success": result.modified_count > 0}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def mark_as_read(alert_id):
        """Mark alert as read"""
        try:
            result = GeofenceAlert.collection.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": {"is_read": True, "updated_at": datetime.utcnow()}}
            )
            return {"success": result.modified_count > 0}
        except Exception as e:
            return {"success": False, "message": str(e)}
