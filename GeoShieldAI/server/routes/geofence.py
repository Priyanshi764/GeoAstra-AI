"""
Geofence Routes for GeoShield AI
API endpoints for cyber zones, geofence alerts, investigation cases, and asset registry
"""
from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime
from routes.auth import token_required, admin_required
from models.geofence_alert import GeofenceAlert
from models.investigation_case import InvestigationCase
from models.cyber_zone import CyberZone
from models.protected_asset import ProtectedAsset
from services.cyber_zone_service import CyberZoneService
from database.mongodb import db

geofence_bp = Blueprint('geofence', __name__, url_prefix='/api/geofence')

# ----------------- GEOFENCE ALERTS -----------------

@geofence_bp.route('/alerts', methods=['GET'])
@token_required
def get_alerts():
    """Get geofence alerts with pagination and filters"""
    try:
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        severity = request.args.get('severity', None)
        status = request.args.get('status', None)
        district = request.args.get('district', None)
        
        query = {}
        if severity:
            query['severity'] = severity
        if status:
            query['status'] = status
        if district:
            query['district'] = district
            
        alerts = GeofenceAlert.get_all_alerts(limit=limit, skip=skip, query=query)
        total = db.geofence_alerts.count_documents(query)
        
        return jsonify({
            "success": True,
            "alerts": alerts,
            "total": total,
            "count": len(alerts)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/alerts/<alert_id>', methods=['GET'])
@token_required
def get_alert_details(alert_id):
    """Get a specific geofence alert details"""
    try:
        alert = GeofenceAlert.get_alert_by_id(alert_id)
        if not alert:
            return jsonify({"success": False, "message": "Alert not found"}), 404
            
        return jsonify({
            "success": True,
            "alert": alert
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/alerts/<alert_id>/status', methods=['PUT'])
@token_required
def update_alert_status(alert_id):
    """Update geofence alert status (e.g. acknowledge or resolve)"""
    try:
        data = request.get_json() or {}
        status = data.get('status')
        if not status:
            return jsonify({"success": False, "message": "Status parameter is required"}), 400
            
        valid_statuses = ['new', 'acknowledged', 'investigating', 'resolved']
        if status not in valid_statuses:
            return jsonify({"success": False, "message": f"Invalid status. Must be one of: {valid_statuses}"}), 400
            
        result = GeofenceAlert.update_alert_status(alert_id, status, request.user.get('user_id'))
        
        # Trigger updates to zones when resolved to recalculate active incidents
        alert = GeofenceAlert.get_alert_by_id(alert_id)
        if alert and alert.get('district'):
            CyberZoneService.get_zone_status(alert['district'])
            
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/alerts/<alert_id>/read', methods=['PUT'])
@token_required
def mark_alert_as_read(alert_id):
    """Mark alert as read"""
    try:
        result = GeofenceAlert.mark_as_read(alert_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ----------------- CYBER ZONES -----------------

@geofence_bp.route('/zones', methods=['GET'])
@token_required
def get_all_cyber_zones():
    """Get all cyber zones and their aggregated risk statuses"""
    try:
        zones = CyberZoneService.get_all_zones()
        return jsonify({
            "success": True,
            "zones": zones
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/zones/<district>', methods=['GET'])
@token_required
def get_cyber_zone_details(district):
    """Get status of a specific district cyber zone"""
    try:
        status = CyberZoneService.get_zone_status(district)
        return jsonify({
            "success": True,
            "zone": status
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ----------------- INVESTIGATION CASES -----------------

@geofence_bp.route('/cases', methods=['GET'])
@token_required
def get_all_investigation_cases():
    """List all auto-created investigation cases"""
    try:
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        status = request.args.get('status', None)
        district = request.args.get('district', None)
        
        query = {}
        if status:
            query['status'] = status
        if district:
            query['district'] = district
            
        cases = InvestigationCase.get_all_cases(limit=limit, skip=skip, query=query)
        total = db.investigation_cases.count_documents(query)
        
        return jsonify({
            "success": True,
            "cases": cases,
            "total": total,
            "count": len(cases)
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/cases/<case_id>', methods=['GET'])
@token_required
def get_case_details(case_id):
    """Get investigation case details with its history timeline"""
    try:
        case = InvestigationCase.get_case_by_id(case_id)
        if not case:
            return jsonify({"success": False, "message": "Case not found"}), 404
            
        return jsonify({
            "success": True,
            "case": case
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/cases/<case_id>/status', methods=['PUT'])
@token_required
def update_case_status(case_id):
    """Update status of a case"""
    try:
        data = request.get_json() or {}
        status = data.get('status')
        if not status:
            return jsonify({"success": False, "message": "Status parameter is required"}), 400
            
        valid_statuses = ['Open', 'Assigned', 'In Progress', 'Resolved']
        if status not in valid_statuses:
            return jsonify({"success": False, "message": f"Invalid status. Must be: {valid_statuses}"}), 400
            
        result = InvestigationCase.update_case_status(case_id, status)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/cases/<case_id>/assign', methods=['PUT'])
@token_required
def assign_case_officer(case_id):
    """Assign case to an officer"""
    try:
        data = request.get_json() or {}
        officer = data.get('officer')
        if not officer:
            return jsonify({"success": False, "message": "Officer name is required"}), 400
            
        result = InvestigationCase.assign_officer(case_id, officer)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ----------------- PROTECTED ASSET REGISTRY -----------------

@geofence_bp.route('/assets', methods=['GET'])
@token_required
def get_assets():
    """Get all protected assets in the registry"""
    try:
        assets = ProtectedAsset.get_all_assets()
        return jsonify({
            "success": True,
            "assets": assets
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/assets', methods=['POST'])
@token_required
@admin_required
def add_protected_asset():
    """Add a new asset to the registry"""
    try:
        data = request.get_json() or {}
        required = ['name', 'type', 'district', 'criticality']
        if not all(k in data for k in required):
            return jsonify({"success": False, "message": f"Missing required fields: {required}"}), 400
            
        result = ProtectedAsset.create_asset(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@geofence_bp.route('/assets/<asset_id>', methods=['PUT'])
@token_required
@admin_required
def update_protected_asset(asset_id):
    """Update asset registry item"""
    try:
        data = request.get_json() or {}
        data['updated_at'] = datetime.utcnow()
        
        result = ProtectedAsset.collection.update_one(
            {"_id": ObjectId(asset_id)},
            {"$set": data}
        )
        return jsonify({"success": result.modified_count > 0}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ----------------- GEOFENCE DASHBOARD STATS -----------------

@geofence_bp.route('/dashboard', methods=['GET'])
@token_required
def get_geofence_dashboard_stats():
    """Aggregated geofence module summary"""
    try:
        total_alerts = db.geofence_alerts.count_documents({})
        new_alerts = db.geofence_alerts.count_documents({"status": "new"})
        active_incidents = db.geofence_alerts.count_documents({"status": {"$ne": "resolved"}})
        
        critical_alerts = db.geofence_alerts.count_documents({"severity": "critical"})
        high_alerts = db.geofence_alerts.count_documents({"severity": "high"})
        
        total_cases = db.investigation_cases.count_documents({})
        open_cases = db.investigation_cases.count_documents({"status": "Open"})
        
        total_assets = db.protected_assets.count_documents({"is_active": True})
        
        # Calculate overall regional threat level from active zones
        zones = CyberZoneService.get_all_zones()
        critical_zones = sum(1 for z in zones if z["risk_level"] == "critical")
        high_zones = sum(1 for z in zones if z["risk_level"] == "high")
        
        return jsonify({
            "success": True,
            "stats": {
                "total_alerts": total_alerts,
                "new_alerts": new_alerts,
                "active_incidents": active_incidents,
                "critical_alerts": critical_alerts,
                "high_alerts": high_alerts,
                "total_cases": total_cases,
                "open_cases": open_cases,
                "total_assets": total_assets,
                "critical_zones": critical_zones,
                "high_zones": high_zones
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
