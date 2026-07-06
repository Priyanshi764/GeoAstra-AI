"""
Geofence Engine for GeoShield AI
Orchestrates the entire intelligence-based geofence threat response pipeline
"""
from models.threat import Threat
from services.asset_matcher import AssetMatcher
from services.dynamic_risk_scorer import DynamicRiskScorer
from services.alert_service import AlertService
from services.case_service import CaseService
from services.cyber_zone_service import CyberZoneService
from services.socket_service import SocketService

class GeofenceEngine:
    """Orchestrator for Intelligence-Based Cyber Geofencing"""
    
    @staticmethod
    def process_threat(threat_id, analysis, organizations, districts, raw_text=""):
        """
        Orchestrate threat processing pipeline:
        Asset Matching -> Dynamic Risk Calculation -> Alert Gen -> Auto Case -> Zone Update -> Socket Emit
        """
        try:
            print(f"[GEOFENCE ENGINE] Starting processing for Threat ID: {threat_id}")
            
            # 1. Match threat entities against Protected Assets
            matched_assets = AssetMatcher.match_assets(organizations, districts, raw_text)
            matched_asset_ids = [a["asset_id"] for a in matched_assets]
            matched_asset_names = [a["asset_name"] for a in matched_assets]
            print(f"[GEOFENCE ENGINE] Matched {len(matched_assets)} protected assets: {matched_asset_names}")
            
            # 2. Calculate dynamic risk score (0-100) and severity level
            risk_info = DynamicRiskScorer.calculate_score(analysis, matched_assets, districts, organizations)
            print(f"[GEOFENCE ENGINE] Dynamic Risk Calculated: {risk_info['score']} ({risk_info['level']})")
            
            # 3. Update the threat record with computed geofence info
            from database.mongodb import db
            from bson.objectid import ObjectId
            
            # Save risk score and matched assets details inside threat collection
            db.threats.update_one(
                {"_id": ObjectId(threat_id)},
                {"$set": {
                    "risk_score_original": analysis.get("risk_score", 0), # Preserve original
                    "risk_score": float(risk_info["score"]) / 10.0,      # Store out of 10 for dashboard compatibility
                    "risk_score_100": risk_info["score"],                # Store out of 100 for geofence module
                    "risk_level": risk_info["level"],
                    "matched_assets": matched_assets,
                    "matched_asset_ids": matched_asset_ids,
                    "matched_asset_names": matched_asset_names
                }}
            )
            
            # 4. Generate Geofence Alerts grouped by district
            alerts = AlertService.generate_alerts_for_threat(threat_id, analysis, matched_assets, risk_info, districts)
            print(f"[GEOFENCE ENGINE] Generated {len(alerts)} Cyber Geofence Alerts.")
            
            # 5. Automatically create Investigation Cases for High/Critical alerts
            cases_created = 0
            for alert in alerts:
                case_id = CaseService.auto_create_case_if_needed(alert)
                if case_id:
                    cases_created += 1
                    
            print(f"[GEOFENCE ENGINE] Automatically created {cases_created} Investigation Cases.")
            
            # 6. Update Cyber Zone status for all affected districts
            for dist in districts:
                CyberZoneService.update_zone_on_trigger(
                    district=dist,
                    threat_risk_score=risk_info["score"],
                    risk_level=risk_info["level"]
                )
            
            # Update specific asset districts if not covered in explicit districts
            for asset in matched_assets:
                asset_dist = asset.get("district")
                if asset_dist and asset_dist not in districts:
                    CyberZoneService.update_zone_on_trigger(
                        district=asset_dist,
                        threat_risk_score=risk_info["score"],
                        risk_level=risk_info["level"]
                    )
            
            # 7. Broadcast Socket.IO events for live update without page refresh
            SocketService.broadcast_event("geofence_triggered", {
                "threat_id": threat_id,
                "risk_score": risk_info["score"],
                "risk_level": risk_info["level"],
                "alerts": alerts,
                "districts": districts,
                "organizations": organizations,
                "matched_assets": matched_asset_names
            })
            
            # Broadcast general refresh signal
            SocketService.broadcast_event("dashboard_refresh", {"timestamp": db.command("ping")})
            
            print(f"[GEOFENCE ENGINE] Processing completed successfully for Threat ID: {threat_id}")
            return {
                "success": True,
                "matched_assets": matched_asset_names,
                "risk_score": risk_info["score"],
                "risk_level": risk_info["level"],
                "alerts_created": len(alerts),
                "cases_created": cases_created
            }
            
        except Exception as e:
            print(f"[GEOFENCE ENGINE] Critical processing error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "message": str(e)}
