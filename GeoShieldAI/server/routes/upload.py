"""
Upload Routes for GeoShield AI
Handles document uploads and threat intelligence processing
"""
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from routes.auth import token_required, admin_required
from services.document_parser import DocumentParser
from ai.gemini_analyzer import GeminiAnalyzer
from ai.entity_mapper import EntityMapper
from ai.risk_engine import RiskEngine
from models.threat import Threat
from models.alert import Alert
from models.protected_asset import ProtectedAsset
from services.geofence_engine import GeofenceEngine

upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'csv', 'json', 'docx'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/document', methods=['POST'])
@token_required
def upload_document():
    """Upload and process threat intelligence document"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "message": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({"success": False, "message": "File size exceeds 50MB limit"}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        
        upload_folder = os.getenv("UPLOAD_FOLDER", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Parse file
        file_extension = filename.rsplit('.', 1)[1].lower()
        parse_result = DocumentParser.parse_file(file_path, file_extension)
        
        if not parse_result['success']:
            os.remove(file_path)
            return jsonify(parse_result), 400
        
        # Extract text content
        if 'text' in parse_result:
            text_content = parse_result['text']
        elif 'data' in parse_result:
            if isinstance(parse_result['data'], list):
                text_content = DocumentParser.extract_text_from_csv_rows(parse_result['data'])
            else:
                text_content = DocumentParser.extract_text_from_json(parse_result['data'])
        else:
            text_content = ""
        
        # Analyze with Gemini
        analysis_result = GeminiAnalyzer.analyze_intelligence(text_content)
        
        if not analysis_result['success']:
            os.remove(file_path)
            return jsonify(analysis_result), 400
        
        analysis = analysis_result['analysis']
        
        # Extract organizations and locations
        org_result = GeminiAnalyzer.extract_organizations(text_content)
        loc_result = GeminiAnalyzer.extract_locations(text_content)
        
        organizations = org_result.get('organizations', [])
        locations = loc_result.get('locations', [])
        
        # Map entities to districts and assets
        mapping = EntityMapper.map_intelligence(locations, organizations)
        
        # Match assets
        matched_assets = ProtectedAsset.collection.find({
            "name": {"$in": organizations}
        })
        asset_ids = [str(asset['_id']) for asset in matched_assets]
        
        # Calculate risk score
        risk_score = RiskEngine.calculate_risk_score(analysis, asset_ids, mapping['districts'])
        alert_severity = RiskEngine.calculate_alert_severity(risk_score)
        
        # Create threat record
        threat_data = {
            "source": request.form.get("source", "file_upload"),
            "threat_type": analysis.get("threat_type", "Unknown"),
            "category": analysis.get("category", "Other"),
            "risk_score": risk_score,
            "confidence": analysis.get("confidence", 0),
            "summary": analysis.get("summary", ""),
            "recommendation": analysis.get("recommendation", ""),
            "mitre_attack": analysis.get("mitre_attack", []),
            "organizations": organizations,
            "districts": mapping['districts'],
            "state": "Madhya Pradesh",
            "threat_actors": analysis.get("threat_actors", []),
            "attack_vector": analysis.get("attack_vector", ""),
            "malware_family": analysis.get("malware_family", ""),
            "iocs": analysis.get("indicators_of_compromise", {}),
            "created_by": request.user['user_id'],
            "file_path": file_path,
            "file_name": filename
        }
        
        threat_result = Threat.create_threat(threat_data)
        
        if not threat_result['success']:
            os.remove(file_path)
            return jsonify(threat_result), 500
        
        threat_id = threat_result['threat_id']
        
        # Create alerts for matched assets
        for asset in mapping['assets']:
            alert_data = {
                "threat_id": threat_id,
                "title": f"New {analysis.get('threat_type', 'Security')} Threat Detected",
                "description": analysis.get("summary", ""),
                "severity": alert_severity,
                "category": analysis.get("category", ""),
                "organization": asset['asset_name'],
                "district": asset['district'],
                "affected_assets": [asset['asset_id']],
                "recommended_action": analysis.get("recommendation", "")
            }
            Alert.create_alert(alert_data)
        
        # Trigger Geofence Engine processing
        GeofenceEngine.process_threat(threat_id, analysis, organizations, mapping['districts'], text_content)
        
        return jsonify({
            "success": True,
            "threat_id": threat_id,
            "message": "Intelligence processed successfully",
            "analysis": {
                "risk_score": risk_score,
                "severity": alert_severity,
                "organizations": organizations,
                "districts": mapping['districts'],
                "threat_type": analysis.get("threat_type", ""),
                "category": analysis.get("category", ""),
                "summary": analysis.get("summary", "")
            }
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@upload_bp.route('/manual', methods=['POST'])
@token_required
def upload_manual_intelligence():
    """Process manually entered threat intelligence"""
    try:
        data = request.get_json()
        
        if not data.get('intelligence_text'):
            return jsonify({"success": False, "message": "No intelligence text provided"}), 400
        
        text_content = data['intelligence_text']
        
        # Analyze with Gemini
        analysis_result = GeminiAnalyzer.analyze_intelligence(text_content)
        
        if not analysis_result['success']:
            return jsonify(analysis_result), 400
        
        analysis = analysis_result['analysis']
        
        # Extract organizations and locations
        org_result = GeminiAnalyzer.extract_organizations(text_content)
        loc_result = GeminiAnalyzer.extract_locations(text_content)
        
        organizations = org_result.get('organizations', [])
        locations = loc_result.get('locations', [])
        
        # Map entities
        mapping = EntityMapper.map_intelligence(locations, organizations)
        
        # Match assets
        matched_assets = list(ProtectedAsset.collection.find({
            "name": {"$in": organizations}
        }))
        asset_ids = [str(asset['_id']) for asset in matched_assets]
        
        # Calculate risk score
        risk_score = RiskEngine.calculate_risk_score(analysis, asset_ids, mapping['districts'])
        alert_severity = RiskEngine.calculate_alert_severity(risk_score)
        
        # Create threat record
        threat_data = {
            "source": "manual_entry",
            "threat_type": analysis.get("threat_type", "Unknown"),
            "category": analysis.get("category", "Other"),
            "risk_score": risk_score,
            "confidence": analysis.get("confidence", 0),
            "summary": analysis.get("summary", ""),
            "recommendation": analysis.get("recommendation", ""),
            "mitre_attack": analysis.get("mitre_attack", []),
            "organizations": organizations,
            "districts": mapping['districts'],
            "state": "Madhya Pradesh",
            "threat_actors": analysis.get("threat_actors", []),
            "attack_vector": analysis.get("attack_vector", ""),
            "malware_family": analysis.get("malware_family", ""),
            "iocs": analysis.get("indicators_of_compromise", {}),
            "created_by": request.user['user_id']
        }
        
        threat_result = Threat.create_threat(threat_data)
        
        if not threat_result['success']:
            return jsonify(threat_result), 500
        
        threat_id = threat_result['threat_id']
        
        # Create alerts for matched assets
        for asset in mapping['assets']:
            alert_data = {
                "threat_id": threat_id,
                "title": f"New {analysis.get('threat_type', 'Security')} Threat Detected",
                "description": analysis.get("summary", ""),
                "severity": alert_severity,
                "category": analysis.get("category", ""),
                "organization": asset['asset_name'],
                "district": asset['district'],
                "affected_assets": [asset['asset_id']],
                "recommended_action": analysis.get("recommendation", "")
            }
            Alert.create_alert(alert_data)
            
        # Trigger Geofence Engine processing
        GeofenceEngine.process_threat(threat_id, analysis, organizations, mapping['districts'], text_content)
        
        return jsonify({
            "success": True,
            "threat_id": threat_id,
            "message": "Intelligence processed successfully",
            "analysis": {
                "risk_score": risk_score,
                "severity": alert_severity,
                "organizations": organizations,
                "districts": mapping['districts'],
                "threat_type": analysis.get("threat_type", ""),
                "category": analysis.get("category", "")
            }
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
