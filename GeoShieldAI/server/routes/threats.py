"""
Threats Routes for GeoShield AI
Handles threat queries and filtering
"""
from flask import Blueprint, request, jsonify
from routes.auth import token_required
from models.threat import Threat
from models.alert import Alert
from models.protected_asset import ProtectedAsset

threats_bp = Blueprint('threats', __name__, url_prefix='/api/threats')

@threats_bp.route('', methods=['GET'])
@token_required
def get_threats():
    """Get all threats with filtering and pagination"""
    try:
        limit = int(request.args.get('limit', 50))
        skip = int(request.args.get('skip', 0))
        district = request.args.get('district', None)
        category = request.args.get('category', None)
        min_risk = int(request.args.get('min_risk', 0))
        
        query = {}
        
        if district:
            query['districts'] = district
        if category:
            query['category'] = category
        if min_risk > 0:
            query['risk_score'] = {"$gte": min_risk}
        
        from database.mongodb import db
        threats = list(db.threats.find(query).sort("created_at", -1).skip(skip).limit(limit))
        total = db.threats.count_documents(query)
        
        for threat in threats:
            threat["_id"] = str(threat["_id"])
        
        return jsonify({
            "success": True,
            "threats": threats,
            "total": total,
            "count": len(threats)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@threats_bp.route('/<threat_id>', methods=['GET'])
@token_required
def get_threat(threat_id):
    """Get specific threat details"""
    try:
        threat = Threat.get_threat_by_id(threat_id)
        
        if not threat:
            return jsonify({"success": False, "message": "Threat not found"}), 404
        
        # Get related alerts
        related_alerts = Alert.collection.find({"threat_id": threat_id})
        alerts = []
        for alert in related_alerts:
            alert["_id"] = str(alert["_id"])
            alerts.append(alert)
        
        threat['related_alerts'] = alerts
        
        return jsonify({
            "success": True,
            "threat": threat
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@threats_bp.route('/district/<district>', methods=['GET'])
@token_required
def get_threats_by_district(district):
    """Get all threats for a specific district"""
    try:
        threats = Threat.get_threats_by_district(district)
        
        return jsonify({
            "success": True,
            "district": district,
            "threats": threats,
            "count": len(threats)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@threats_bp.route('/organization/<organization>', methods=['GET'])
@token_required
def get_threats_by_organization(organization):
    """Get all threats for a specific organization"""
    try:
        threats = Threat.get_threats_by_organization(organization)
        
        return jsonify({
            "success": True,
            "organization": organization,
            "threats": threats,
            "count": len(threats)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@threats_bp.route('/high-risk', methods=['GET'])
@token_required
def get_high_risk_threats():
    """Get all high-risk threats"""
    try:
        threats = Threat.get_high_risk_threats()
        
        return jsonify({
            "success": True,
            "threats": threats,
            "count": len(threats)
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@threats_bp.route('/<threat_id>/update', methods=['PUT'])
@token_required
def update_threat(threat_id):
    """Update threat status or notes"""
    try:
        data = request.get_json()
        update_data = {}
        
        if 'status' in data:
            update_data['status'] = data['status']
        if 'notes' in data:
            update_data['notes'] = data['notes']
        
        if not update_data:
            return jsonify({"success": False, "message": "No update data provided"}), 400
        
        result = Threat.update_threat(threat_id, update_data)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
