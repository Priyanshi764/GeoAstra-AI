"""
GeoAstra AI Backend
AI-Powered Dark Web Geofencing & Cyber Threat Intelligence Platform
"""
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime

# Import blueprints
from routes.auth import auth_bp
from routes.upload import upload_bp
from routes.dashboard import dashboard_bp
from routes.threats import threats_bp
from routes.alerts import alerts_bp
from routes.assistant import assistant_bp
from routes.user import user_bp
from routes.geofence import geofence_bp

import socketio
from services.socket_service import sio

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Enable CORS for all routes (to support socket.io /socket.io/)
CORS(app, resources={r"/*": {"origins": "*"}})

# Wrap WSGI handler
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(threats_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(assistant_bp)
app.register_blueprint(user_bp)
app.register_blueprint(geofence_bp)

# Root routes
@app.route("/", methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        "message": "GeoAstra AI Backend Running",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route("/health", methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Check MongoDB connection
        from database.mongodb import db
        db.command('ping')
        mongo_status = "connected"
    except:
        mongo_status = "disconnected"
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "operational",
            "mongodb": mongo_status
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint not found",
        "status": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "message": "Internal server error",
        "status": 500
    }), 500

if __name__ == "__main__":
    # Initialize protected assets if needed
    from models.protected_asset import ProtectedAsset
    from database.mongodb import db
    
    # Create default protected assets if they don't exist
    if db.protected_assets.count_documents({}) == 0:
        default_assets = [
            {
                "name": "IIITDM Jabalpur",
                "type": "University",
                "district": "Jabalpur",
                "state": "Madhya Pradesh",
                "address": "Dumna Road, Jabalpur, MP",
                "latitude": 23.1815,
                "longitude": 79.9864,
                "criticality": "critical",
                "sectors": ["Education", "Research", "Critical Technology"]
            },
            {
                "name": "AIIMS Bhopal",
                "type": "Hospital",
                "district": "Bhopal",
                "state": "Madhya Pradesh",
                "address": "Saket Nagar, Bhopal, MP",
                "latitude": 23.1815,
                "longitude": 77.4104,
                "criticality": "critical",
                "sectors": ["Healthcare", "Emergency Services"]
            },
            {
                "name": "SBI Regional Office",
                "type": "Bank",
                "district": "Jabalpur",
                "state": "Madhya Pradesh",
                "address": "Civil Lines, Jabalpur, MP",
                "latitude": 23.1678,
                "longitude": 79.9542,
                "criticality": "high",
                "sectors": ["Finance", "Banking"]
            },
            {
                "name": "Collector Office Indore",
                "type": "Government",
                "district": "Indore",
                "state": "Madhya Pradesh",
                "address": "Collectorate Road, Indore, MP",
                "latitude": 22.7196,
                "longitude": 75.8577,
                "criticality": "critical",
                "sectors": ["Government", "Administration"]
            },
            {
                "name": "Police Headquarters Jabalpur",
                "type": "Police",
                "district": "Jabalpur",
                "state": "Madhya Pradesh",
                "address": "South Civil Lines, Jabalpur, MP",
                "latitude": 23.1601,
                "longitude": 79.9610,
                "criticality": "critical",
                "sectors": ["Public Safety", "Law Enforcement"]
            },
            {
                "name": "Municipal Corporation Bhopal",
                "type": "Government",
                "district": "Bhopal",
                "state": "Madhya Pradesh",
                "address": "Link Road No. 1, Bhopal, MP",
                "latitude": 23.2324,
                "longitude": 77.4278,
                "criticality": "high",
                "sectors": ["Municipal", "Government"]
            },
            {
                "name": "High Court Gwalior",
                "type": "Government",
                "district": "Gwalior",
                "state": "Madhya Pradesh",
                "address": "City Center, Gwalior, MP",
                "latitude": 26.2038,
                "longitude": 78.1962,
                "criticality": "critical",
                "sectors": ["Judiciary", "Government"]
            },
            {
                "name": "Mahakaleshwar Temple Trust Ujjain",
                "type": "Government",
                "district": "Ujjain",
                "state": "Madhya Pradesh",
                "address": "Mahakal Marg, Ujjain, MP",
                "latitude": 23.1829,
                "longitude": 75.7682,
                "criticality": "high",
                "sectors": ["Public Infrastructure", "Tourism"]
            },
            {
                "name": "Choithram Hospital Indore",
                "type": "Hospital",
                "district": "Indore",
                "state": "Madhya Pradesh",
                "address": "Manik Bagh Road, Indore, MP",
                "latitude": 22.6953,
                "longitude": 75.8458,
                "criticality": "critical",
                "sectors": ["Healthcare"]
            },
            {
                "name": "SBI Regional Office Indore",
                "type": "Bank",
                "district": "Indore",
                "state": "Madhya Pradesh",
                "address": "Khamla, Indore, MP",
                "latitude": 22.7250,
                "longitude": 75.8650,
                "criticality": "high",
                "sectors": ["Finance", "Banking"]
            },
            {
                "name": "Netaji Subhash Chandra Bose Medical College Jabalpur",
                "type": "Hospital",
                "district": "Jabalpur",
                "state": "Madhya Pradesh",
                "address": "Tilwara Road, Jabalpur, MP",
                "latitude": 23.1492,
                "longitude": 79.9004,
                "criticality": "critical",
                "sectors": ["Healthcare", "Education"]
            },
            {
                "name": "Police Headquarters Bhopal",
                "type": "Police",
                "district": "Bhopal",
                "state": "Madhya Pradesh",
                "address": "Jahangirabad, Bhopal, MP",
                "latitude": 23.2423,
                "longitude": 77.4190,
                "criticality": "critical",
                "sectors": ["Public Safety", "Law Enforcement"]
            },
            {
                "name": "Municipal Corporation Indore",
                "type": "Government",
                "district": "Indore",
                "state": "Madhya Pradesh",
                "address": "MG Road, Indore, MP",
                "latitude": 22.7230,
                "longitude": 75.8620,
                "criticality": "high",
                "sectors": ["Municipal", "Government"]
            }
        ]
        
        for asset in default_assets:
            ProtectedAsset.create_asset(asset)
        
        print("Default protected assets created")
        
    # Initialize cyber zones if needed
    if db.cyber_zones.count_documents({}) == 0:
        from services.cyber_zone_service import CyberZoneService, MP_DISTRICTS
        print("Initializing cyber zones status in the database...")
        for district in MP_DISTRICTS:
            CyberZoneService.get_zone_status(district)
        print("Cyber zones initialized successfully")
        
    # Start the Threat Intelligence Ingestion Engine Background Scheduler
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
        from apscheduler.schedulers.background import BackgroundScheduler
        from services.ingestion.engine import IngestionEngine
        
        ingestion_engine = IngestionEngine()
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=ingestion_engine.run_cycle, trigger="interval", minutes=2)
        scheduler.start()
        print("Threat Intelligence Ingestion Scheduler started (running every 2 minutes).")
        
        # Optionally, kick off an immediate run in a separate thread so it doesn't block startup
        import threading
        threading.Thread(target=ingestion_engine.run_cycle, daemon=True).start()
    
    app.run(debug=os.getenv("DEBUG", "True") == "True", port=5000)