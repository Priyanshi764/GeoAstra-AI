"""
Case Service for GeoShield AI
Manages automated creation of Investigation Cases for High/Critical risk triggers
"""
from models.investigation_case import InvestigationCase
from models.threat import Threat

class CaseService:
    """Manages creation and updates of Investigation Cases"""
    
    @staticmethod
    def auto_create_case_if_needed(alert):
        """
        Check alert risk level and auto-create an Investigation Case
        if severity is High or Critical.
        """
        severity = alert.get("severity", "medium").lower()
        if severity not in ["high", "critical"]:
            return None
            
        try:
            # 1. Fetch threat details
            threat_id = alert.get("threat_id")
            threat = Threat.get_threat_by_id(threat_id)
            
            # Group asset names
            assets = [a.get("asset_name") for a in alert.get("affected_assets", [])]
            
            # Gather evidence (IOCs)
            evidence = {}
            if threat:
                evidence = threat.get("iocs", {})
                
            case_data = {
                "threat_id": threat_id,
                "alert_id": alert.get("_id"),
                "title": f"Investigation: {alert.get('zone', 'Region')} Security Incident",
                "threat_type": threat.get("threat_type", "Unknown") if threat else "Unknown",
                "category": alert.get("category", "Other"),
                "risk_score": alert.get("risk_score", 70.0),
                "risk_level": severity,
                "district": alert.get("district", ""),
                "affected_assets": assets,
                "summary": alert.get("description", ""),
                "evidence": evidence,
                "recommended_actions": alert.get("recommended_actions", []),
                "status": "Open",
                "source": threat.get("source", "System") if threat else "System"
            }
            
            res = InvestigationCase.create_case(case_data)
            if res["success"]:
                return res["case_id"]
            return None
        except Exception as e:
            print(f"[CASE SERVICE] Error creating case: {str(e)}")
            return None
