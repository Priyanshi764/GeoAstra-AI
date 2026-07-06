"""
Alerts Routes for GeoShield AI
Handles alert management and notifications
"""
from flask import Blueprint, request, jsonify
from routes.auth import token_required
from models.alert import Alert
from models.threat import Threat

alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@alerts_bp.route('', methods=['GET'])
@token_required
def get_alerts():
    """Get all alerts with filtering"""
    try:
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        severity = request.args.get('severity', None)
        status = request.args.get('status', None)
        is_read = request.args.get('is_read', None)
        
        query = {}
        
        if severity:
            query['severity'] = severity
        if status:
            query['status'] = status
        if is_read is not None:
            query['is_read'] = is_read == 'true'
        
        from database.mongodb import db
        alerts = list(db.alerts.find(query).sort("created_at", -1).skip(skip).limit(limit))
        total = db.alerts.count_documents(query)
        
        for alert in alerts:
            alert["_id"] = str(alert["_id"])
        
        return jsonify({
            "success": True,
            "alerts": alerts,
            "total": total,
            "count": len(alerts)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@alerts_bp.route('/<alert_id>', methods=['GET'])
@token_required
def get_alert(alert_id):
    """Get specific alert details"""
    try:
        from bson.objectid import ObjectId
        alert = Alert.collection.find_one({"_id": ObjectId(alert_id)})
        
        if not alert:
            return jsonify({"success": False, "message": "Alert not found"}), 404
        
        alert["_id"] = str(alert["_id"])
        
        # Get related threat if exists
        if alert.get('threat_id'):
            threat = Threat.get_threat_by_id(alert['threat_id'])
            alert['threat'] = threat
        
        return jsonify({
            "success": True,
            "alert": alert
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@alerts_bp.route('/<alert_id>/read', methods=['PUT'])
@token_required
def mark_as_read(alert_id):
    """Mark alert as read"""
    try:
        result = Alert.mark_as_read(alert_id)
        
        if result['success']:
            return jsonify({"success": True, "message": "Alert marked as read"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to mark alert as read"}), 400
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@alerts_bp.route('/<alert_id>/acknowledge', methods=['PUT'])
@token_required
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    try:
        result = Alert.acknowledge_alert(alert_id, request.user['user_id'])
        
        if result['success']:
            return jsonify({"success": True, "message": "Alert acknowledged"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to acknowledge alert"}), 400
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@alerts_bp.route('/<alert_id>/status', methods=['PUT'])
@token_required
def update_alert_status(alert_id):
    """Update alert status"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({"success": False, "message": "Status not provided"}), 400
        
        valid_statuses = ['new', 'acknowledged', 'investigating', 'resolved']
        if status not in valid_statuses:
            return jsonify({"success": False, "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
        
        result = Alert.update_alert_status(alert_id, status)
        
        if result['success']:
            return jsonify({"success": True, "message": f"Alert status updated to {status}"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to update alert status"}), 400
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@alerts_bp.route('/severity/<severity>', methods=['GET'])
@token_required
def get_alerts_by_severity(severity):
    """Get alerts by severity level"""
    try:
        valid_severities = ['low', 'medium', 'high', 'critical']
        if severity not in valid_severities:
            return jsonify({"success": False, "message": f"Invalid severity. Must be one of: {', '.join(valid_severities)}"}), 400
        
        alerts = Alert.get_alerts_by_severity(severity)
        
        return jsonify({
            "success": True,
            "severity": severity,
            "alerts": alerts,
            "count": len(alerts)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@alerts_bp.route('/unread', methods=['GET'])
@token_required
def get_unread_alerts():
    """Get all unread alerts"""
    try:
        alerts = Alert.get_unread_alerts()
        
        return jsonify({
            "success": True,
            "alerts": alerts,
            "count": len(alerts)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@alerts_bp.route('/summary', methods=['GET'])
@token_required
def get_alerts_summary():
    """Get alerts summary"""
    try:
        from database.mongodb import db
        
        total = db.alerts.count_documents({})
        critical = db.alerts.count_documents({"severity": "critical"})
        high = db.alerts.count_documents({"severity": "high"})
        medium = db.alerts.count_documents({"severity": "medium"})
        low = db.alerts.count_documents({"severity": "low"})
        unread = db.alerts.count_documents({"is_read": False})
        
        return jsonify({
            "success": True,
            "summary": {
                "total": total,
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low,
                "unread": unread
            }
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
