"""
Cyber Zone Model for GeoShield AI
Manages zone status and statistics per district
"""
from datetime import datetime
from database.mongodb import db

class CyberZone:
    """Model for managing cyber security zones per district"""
    
    collection = db.cyber_zones
    
    @staticmethod
    def get_or_create_zone(district):
        """Get or initialize a cyber zone for a district"""
        try:
            zone = CyberZone.collection.find_one({"district": district})
            if not zone:
                zone_record = {
                    "district": district,
                    "zone_name": f"{district} Cyber Zone",
                    "threat_count": 0,
                    "risk_score": 0.0,
                    "risk_level": "low",
                    "active_incidents": 0,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                CyberZone.collection.insert_one(zone_record)
                zone = CyberZone.collection.find_one({"district": district})
            
            if zone:
                zone["_id"] = str(zone["_id"])
            return zone
        except Exception as e:
            return None
            
    @staticmethod
    def update_zone_stats(district, risk_score, risk_level, threat_increment=None, incident_increment=None, threat_count=None, active_incidents=None):
        """Update threat count, active incidents, risk score and risk level for a zone"""
        try:
            CyberZone.get_or_create_zone(district)  # Ensure it exists
            
            # Get current values to prevent negative values
            zone = CyberZone.collection.find_one({"district": district})
            
            if threat_count is not None:
                new_threat_count = max(0, threat_count)
            else:
                inc = threat_increment if threat_increment is not None else 1
                new_threat_count = max(0, zone.get("threat_count", 0) + inc)
                
            if active_incidents is not None:
                new_incidents = max(0, active_incidents)
            else:
                inc = incident_increment if incident_increment is not None else 1
                new_incidents = max(0, zone.get("active_incidents", 0) + inc)
            
            result = CyberZone.collection.update_one(
                {"district": district},
                {
                    "$set": {
                        "threat_count": new_threat_count,
                        "active_incidents": new_incidents,
                        "risk_score": float(risk_score),
                        "risk_level": risk_level,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
            
    @staticmethod
    def get_all_zones():
        """Get all cyber zones"""
        try:
            zones = list(CyberZone.collection.find().sort("risk_score", -1))
            for zone in zones:
                zone["_id"] = str(zone["_id"])
            return zones
        except Exception as e:
            return []
