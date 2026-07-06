"""
Investigation Case Model for GeoShield AI
Manages threat investigation cases and timelines
"""
from datetime import datetime
from bson.objectid import ObjectId
from database.mongodb import db

class InvestigationCase:
    """Model for managing threat investigation cases"""
    
    collection = db.investigation_cases
    
    @staticmethod
    def create_case(case_data):
        """Create a new investigation case"""
        try:
            now = datetime.utcnow()
            
            # Default timeline events
            timeline = case_data.get("timeline", [])
            if not timeline:
                timeline = [
                    {
                        "event": "Threat Received",
                        "description": f"Threat intelligence ingest from source: {case_data.get('source', 'System')}",
                        "timestamp": now.isoformat(),
                        "status": "completed"
                    },
                    {
                        "event": "AI Analysis",
                        "description": "Entity extraction and classification finished",
                        "timestamp": now.isoformat(),
                        "status": "completed"
                    },
                    {
                        "event": "Protected Asset Matched",
                        "description": f"Assets matched: {', '.join(case_data.get('affected_assets', ['None']))}",
                        "timestamp": now.isoformat(),
                        "status": "completed"
                    },
                    {
                        "event": "Geofence Triggered",
                        "description": f"Geofence alert created for Cyber Zone: {case_data.get('district', 'General')}",
                        "timestamp": now.isoformat(),
                        "status": "completed"
                    },
                    {
                        "event": "Investigation Case Created",
                        "description": "Auto-case created due to high/critical risk level",
                        "timestamp": now.isoformat(),
                        "status": "completed"
                    }
                ]
                
            case_record = {
                "threat_id": case_data.get("threat_id", ""),
                "alert_id": case_data.get("alert_id", ""),
                "title": case_data.get("title", "Threat Investigation Case"),
                "threat_type": case_data.get("threat_type", "Unknown"),
                "category": case_data.get("category", "Other"),
                "risk_score": case_data.get("risk_score", 50),
                "risk_level": case_data.get("risk_level", "medium"),  # low, medium, high, critical
                "district": case_data.get("district", ""),
                "affected_assets": case_data.get("affected_assets", []),
                "summary": case_data.get("summary", ""),
                "evidence": case_data.get("evidence", {}),  # IOCs, file paths, etc.
                "recommended_actions": case_data.get("recommended_actions", []),
                "assigned_officer": case_data.get("assigned_officer", "Unassigned"),
                "status": case_data.get("status", "Open"),  # Open, Assigned, In Progress, Resolved
                "timeline": timeline,
                "created_at": now,
                "updated_at": now
            }
            
            result = InvestigationCase.collection.insert_one(case_record)
            return {
                "success": True,
                "case_id": str(result.inserted_id),
                "message": "Investigation case created successfully"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
            
    @staticmethod
    def get_all_cases(limit=100, skip=0, query=None):
        """Get all cases with filters and pagination"""
        try:
            search_query = query if query else {}
            cases = list(InvestigationCase.collection.find(search_query).sort("created_at", -1).skip(skip).limit(limit))
            for case in cases:
                case["_id"] = str(case["_id"])
            return cases
        except Exception as e:
            return []
            
    @staticmethod
    def get_case_by_id(case_id):
        """Get specific case by ID"""
        try:
            case = InvestigationCase.collection.find_one({"_id": ObjectId(case_id)})
            if case:
                case["_id"] = str(case["_id"])
            return case
        except Exception as e:
            return None
            
    @staticmethod
    def add_timeline_event(case_id, event_title, description, status="completed"):
        """Add event to case timeline"""
        try:
            event = {
                "event": event_title,
                "description": description,
                "timestamp": datetime.utcnow().isoformat(),
                "status": status
            }
            result = InvestigationCase.collection.update_one(
                {"_id": ObjectId(case_id)},
                {
                    "$push": {"timeline": event},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            return {"success": result.modified_count > 0}
        except Exception as e:
            return {"success": False, "message": str(e)}
            
    @staticmethod
    def update_case_status(case_id, status):
        """Update case status"""
        try:
            result = InvestigationCase.collection.update_one(
                {"_id": ObjectId(case_id)},
                {
                    "$set": {
                        "status": status,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            if result.modified_count > 0:
                InvestigationCase.add_timeline_event(
                    case_id,
                    f"Investigation Status Updated",
                    f"Case status changed to: {status}"
                )
                return {"success": True}
            return {"success": False, "message": "No fields modified"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def assign_officer(case_id, officer_name):
        """Assign officer to case"""
        try:
            result = InvestigationCase.collection.update_one(
                {"_id": ObjectId(case_id)},
                {
                    "$set": {
                        "assigned_officer": officer_name,
                        "status": "Assigned",
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            if result.modified_count > 0:
                InvestigationCase.add_timeline_event(
                    case_id,
                    "Officer Assigned",
                    f"Case assigned to officer: {officer_name}"
                )
                InvestigationCase.add_timeline_event(
                    case_id,
                    "Investigation Started",
                    f"Active investigation started by {officer_name}"
                )
                return {"success": True}
            return {"success": False, "message": "No fields modified"}
        except Exception as e:
            return {"success": False, "message": str(e)}
