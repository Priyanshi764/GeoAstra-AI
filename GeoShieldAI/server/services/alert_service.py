"""
Alert Service for GeoShield AI
Compiles and creates detailed Geofence Alerts
"""
from models.geofence_alert import GeofenceAlert

class AlertService:
    """Generates richly structured Cyber Geofence Alerts"""
    
    @staticmethod
    def generate_alerts_for_threat(threat_id, analysis, matched_assets, risk_info, districts):
        """
        Group matched assets by district and create GeofenceAlert records.
        Returns a list of created alert details.
        """
        created_alerts = []
        
        # 1. Group matched assets by district
        district_assets = {}
        for asset in matched_assets:
            dist = asset.get("district")
            if dist:
                if dist not in district_assets:
                    district_assets[dist] = []
                district_assets[dist].append(asset)
                
        # If no districts matched but we have extracted districts, make sure we cover them too
        for dist in districts:
            if dist not in district_assets:
                district_assets[dist] = [] # Empty list of matched assets but zone is still affected
                
        # 2. For each affected district, generate a Geofence Alert
        threat_type = analysis.get("threat_type", "Security Threat")
        confidence = analysis.get("confidence", 50)
        iocs = analysis.get("indicators_of_compromise", {})
        
        for district, assets in district_assets.items():
            zone_name = f"{district} Cyber Zone"
            
            # Build recommended actions dynamically
            actions = [
                "Notify District Cyber Cell",
            ]
            
            # Asset-specific notifications
            for asset in assets:
                actions.append(f"Notify {asset.get('asset_name')} SOC")
                
            # IOC actions
            if iocs.get("apk_packages"):
                for apk in iocs["apk_packages"][:2]:
                    actions.append(f"Block APK: {apk}")
            elif iocs.get("urls") or iocs.get("domains"):
                actions.append("Block malicious URL/Domain connections")
                
            if iocs.get("ips"):
                actions.append("Block threat actor IP addresses on firewalls")
                
            # Escalation actions
            if risk_info["level"] in ["high", "critical"]:
                actions.append("Generate Incident Investigation Case")
                actions.append("Isolate affected segments")
            
            description = f"Geofence breach detected in {zone_name}. AI threat analyzer identified targeted campaign: {analysis.get('summary', 'Suspicious activity detected.')}"
            
            alert_data = {
                "threat_id": threat_id,
                "title": f"🚨 CYBER GEOFENCE ALERT: {zone_name}",
                "description": description,
                "severity": risk_info["level"], # low, medium, high, critical
                "risk_score": risk_info["score"],
                "confidence": confidence,
                "zone": zone_name,
                "district": district,
                "affected_assets": [
                    {
                        "asset_id": a["asset_id"],
                        "asset_name": a["asset_name"],
                        "type": a["type"],
                        "criticality": a["criticality"],
                        "match_score": a["match_score"]
                    } for a in assets
                ],
                "recommended_actions": actions,
                "status": "new"
            }
            
            res = GeofenceAlert.create_alert(alert_data)
            if res["success"]:
                alert_data["_id"] = res["alert_id"]
                created_alerts.append(alert_data)
                
        return created_alerts
