"""
Threat Model for GeoShield AI
Handles threat intelligence storage and retrieval
"""
from datetime import datetime
from bson.objectid import ObjectId
from database.mongodb import db

class Threat:
    """Threat model for storing cyber intelligence"""
    
    collection = db.threats
    
    @staticmethod
    def create_threat(threat_data):
        """Create a new threat record"""
        try:
            threat_record = {
                "source": threat_data.get("source", "unknown"),
                "threat_type": threat_data.get("threat_type", ""),
                "category": threat_data.get("category", ""),
                "risk_score": threat_data.get("risk_score", 0),
                "confidence": threat_data.get("confidence", 0),
                "summary": threat_data.get("summary", ""),
                "recommendation": threat_data.get("recommendation", ""),
                "mitre_attack": threat_data.get("mitre_attack", []),
                "organizations": threat_data.get("organizations", []),
                "districts": threat_data.get("districts", []),
                "state": threat_data.get("state", "Madhya Pradesh"),
                "threat_actors": threat_data.get("threat_actors", []),
                "attack_vector": threat_data.get("attack_vector", ""),
                "malware_family": threat_data.get("malware_family", ""),
                "iocs": threat_data.get("iocs", {}),
                "created_by": threat_data.get("created_by", "system"),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "status": "active"
            }
            
            result = Threat.collection.insert_one(threat_record)
            return {
                "success": True,
                "threat_id": str(result.inserted_id),
                "message": "Threat created successfully"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def get_all_threats(limit=100, skip=0):
        """Get all threats with pagination"""
        try:
            threats = list(Threat.collection.find().sort("created_at", -1).skip(skip).limit(limit))
            for threat in threats:
                threat["_id"] = str(threat["_id"])
            return threats
        except Exception as e:
            return []
    
    @staticmethod
    def get_threat_by_id(threat_id):
        """Get threat by ID"""
        try:
            threat = Threat.collection.find_one({"_id": ObjectId(threat_id)})
            if threat:
                threat["_id"] = str(threat["_id"])
            return threat
        except Exception as e:
            return None
    
    @staticmethod
    def get_threats_by_district(district):
        """Get threats for a specific district"""
        try:
            threats = list(Threat.collection.find({"districts": district}).sort("created_at", -1))
            for threat in threats:
                threat["_id"] = str(threat["_id"])
            return threats
        except Exception as e:
            return []
    
    @staticmethod
    def get_threats_by_organization(organization):
        """Get threats for a specific organization"""
        try:
            threats = list(Threat.collection.find({"organizations": organization}).sort("created_at", -1))
            for threat in threats:
                threat["_id"] = str(threat["_id"])
            return threats
        except Exception as e:
            return []
    
    @staticmethod
    def get_high_risk_threats():
        """Get all high-risk threats"""
        try:
            threats = list(Threat.collection.find({"risk_score": {"$gte": 7}}).sort("risk_score", -1))
            for threat in threats:
                threat["_id"] = str(threat["_id"])
            return threats
        except Exception as e:
            return []
    
    @staticmethod
    def update_threat(threat_id, update_data):
        """Update threat record"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            result = Threat.collection.update_one(
                {"_id": ObjectId(threat_id)},
                {"$set": update_data}
            )
            return {"success": result.modified_count > 0}
        except Exception as e:
            return {"success": False}
