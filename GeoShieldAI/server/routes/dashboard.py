"""
Dashboard Routes for GeoShield AI
Provides aggregated statistics and intelligence overview
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from routes.auth import token_required
from models.threat import Threat
from models.alert import Alert
from models.protected_asset import ProtectedAsset
from database.mongodb import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/stats', methods=['GET'])
@token_required
def get_stats():
    """Get dashboard statistics"""
    try:
        now = datetime.utcnow()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)
        
        # Alert statistics (Aggregate from both general alerts and geofence alerts)
        total_alerts = db.alerts.count_documents({}) + db.geofence_alerts.count_documents({})
        critical_alerts = db.alerts.count_documents({"severity": "critical"}) + db.geofence_alerts.count_documents({"severity": "critical"})
        high_alerts = db.alerts.count_documents({"severity": "high"}) + db.geofence_alerts.count_documents({"severity": "high"})
        medium_alerts = db.alerts.count_documents({"severity": "medium"}) + db.geofence_alerts.count_documents({"severity": "medium"})
        low_alerts = db.alerts.count_documents({"severity": "low"}) + db.geofence_alerts.count_documents({"severity": "low"})
        
        alerts_24h = db.alerts.count_documents({"created_at": {"$gte": last_24h}}) + db.geofence_alerts.count_documents({"created_at": {"$gte": last_24h}})
        alerts_7d = db.alerts.count_documents({"created_at": {"$gte": last_7d}}) + db.geofence_alerts.count_documents({"created_at": {"$gte": last_7d}})
        unread_alerts = db.alerts.count_documents({"is_read": False}) + db.geofence_alerts.count_documents({"is_read": False})
        
        # Threat statistics
        total_threats = Threat.collection.count_documents({})
        high_risk_threats = Threat.collection.count_documents({"risk_score": {"$gte": 7}})
        threats_24h = Threat.collection.count_documents({"created_at": {"$gte": last_24h}})
        threats_7d = Threat.collection.count_documents({"created_at": {"$gte": last_7d}})
        
        # Protected assets
        total_assets = ProtectedAsset.collection.count_documents({"is_active": True})
        critical_assets = ProtectedAsset.collection.count_documents({
            "criticality": "critical",
            "is_active": True
        })
        
        # Districts with threats
        districts_with_threats = len(db.threats.distinct("districts"))
        
        # Top threat types
        threat_types = list(db.threats.aggregate([
            {"$group": {"_id": "$threat_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]))
        
        # Top threat categories
        threat_categories = list(db.threats.aggregate([
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]))
        
        # Top affected organizations
        top_orgs = list(db.threats.aggregate([
            {"$unwind": "$organizations"},
            {"$group": {"_id": "$organizations", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]))
        
        # Top affected districts
        top_districts = list(db.threats.aggregate([
            {"$unwind": "$districts"},
            {"$group": {"_id": "$districts", "count": {"$sum": 1}, "avg_risk": {"$avg": "$risk_score"}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]))
        
        return jsonify({
            "success": True,
            "stats": {
                "alerts": {
                    "total": total_alerts,
                    "critical": critical_alerts,
                    "high": high_alerts,
                    "medium": medium_alerts,
                    "low": low_alerts,
                    "last_24h": alerts_24h,
                    "last_7d": alerts_7d,
                    "unread": unread_alerts
                },
                "threats": {
                    "total": total_threats,
                    "high_risk": high_risk_threats,
                    "last_24h": threats_24h,
                    "last_7d": threats_7d
                },
                "assets": {
                    "total": total_assets,
                    "critical": critical_assets
                },
                "coverage": {
                    "districts_with_threats": districts_with_threats,
                    "threat_types": threat_types,
                    "threat_categories": threat_categories,
                    "top_organizations": top_orgs,
                    "top_districts": top_districts
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dashboard_bp.route('/recent-threats', methods=['GET'])
@token_required
def get_recent_threats():
    """Get recent threats"""
    try:
        limit = int(request.args.get('limit', 20))
        skip = int(request.args.get('skip', 0))
        
        threats = Threat.get_all_threats(limit=limit, skip=skip)
        
        return jsonify({
            "success": True,
            "threats": threats,
            "count": len(threats)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dashboard_bp.route('/recent-alerts', methods=['GET'])
@token_required
def get_recent_alerts():
    """Get recent alerts"""
    try:
        limit = int(request.args.get('limit', 20))
        skip = int(request.args.get('skip', 0))
        
        alerts = Alert.collection.find().sort("created_at", -1).skip(skip).limit(limit)
        alerts_list = []
        for alert in alerts:
            alert["_id"] = str(alert["_id"])
            alerts_list.append(alert)
        
        return jsonify({
            "success": True,
            "alerts": alerts_list,
            "count": len(alerts_list)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dashboard_bp.route('/threat-timeline', methods=['GET'])
@token_required
def get_threat_timeline():
    """Get threat timeline for last 30 days"""
    try:
        last_30d = datetime.utcnow() - timedelta(days=30)
        
        timeline = list(db.threats.aggregate([
            {"$match": {"created_at": {"$gte": last_30d}}},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                "count": {"$sum": 1},
                "avg_risk": {"$avg": "$risk_score"}
            }},
            {"$sort": {"_id": 1}}
        ]))
        
        return jsonify({
            "success": True,
            "timeline": timeline
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@dashboard_bp.route('/districts-map', methods=['GET'])
@token_required
def get_districts_map():
    """Get threat data by district for map visualization"""
    try:
        district_data = list(db.threats.aggregate([
            {"$unwind": "$districts"},
            {"$group": {
                "_id": "$districts",
                "threat_count": {"$sum": 1},
                "avg_risk": {"$avg": "$risk_score"},
                "high_risk": {"$sum": {"$cond": [{"$gte": ["$risk_score", 7]}, 1, 0]}}
            }},
            {"$sort": {"threat_count": -1}}
        ]))
        
        # Add coordinates for districts (basic MP district coordinates)
        district_coords = {
            "Bhopal": {"lat": 23.1815, "lng": 77.4104},
            "Indore": {"lat": 22.7196, "lng": 75.8577},
            "Jabalpur": {"lat": 23.1815, "lng": 79.9864},
            "Gwalior": {"lat": 26.2183, "lng": 78.1629},
            "Ujjain": {"lat": 23.1815, "lng": 75.7885},
            "Sagar": {"lat": 22.7345, "lng": 78.7733},
            "Nagpur": {"lat": 21.1458, "lng": 79.0882},
            "Ratlam": {"lat": 23.3300, "lng": 75.0450},
            "Morena": {"lat": 25.4274, "lng": 78.0068},
            "Shivpuri": {"lat": 25.4274, "lng": 77.6644},
        }
        
        for district in district_data:
            district_name = district['_id']
            if district_name in district_coords:
                district['coordinates'] = district_coords[district_name]
        
        return jsonify({
            "success": True,
            "districts": district_data
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
