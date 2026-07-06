"""
Risk Scoring Engine for GeoShield AI
Calculates threat risk scores based on multiple factors
"""
from datetime import datetime, timedelta
from database.mongodb import db

class RiskEngine:
    """Calculates risk scores for threats"""
    
    # Risk scoring weights
    WEIGHTS = {
        "threat_category": 0.25,
        "organization_criticality": 0.20,
        "district_sensitivity": 0.15,
        "ioc_count": 0.15,
        "confidence": 0.15,
        "historical_incidents": 0.10
    }
    
    THREAT_CATEGORY_SCORES = {
        "APT": 9,
        "Data Breach": 8,
        "Ransomware": 9,
        "Malware": 7,
        "Phishing": 6,
        "DDoS": 7,
        "Insider Threat": 8,
        "Supply Chain": 7,
        "Vulnerability": 5,
        "Hacktivism": 5,
        "Other": 4
    }
    
    ORGANIZATION_CRITICALITY_SCORES = {
        "critical": 10,
        "high": 8,
        "medium": 5,
        "low": 2
    }
    
    DISTRICT_SENSITIVITY = {
        # Capital districts
        "Bhopal": 10,
        "Indore": 9,
        
        # IT/Tech hubs
        "Jabalpur": 8,
        
        # Administrative centers
        "Gwalior": 8,
        "Ujjain": 7,
        
        # Other significant districts
        "Sagar": 6,
        "Ratlam": 5,
        
        # Others (default)
    }
    
    @staticmethod
    def get_threat_category_score(category):
        """Get risk score for threat category"""
        return RiskEngine.THREAT_CATEGORY_SCORES.get(category, 4)
    
    @staticmethod
    def get_organization_criticality_score(criticality):
        """Get risk score for organization criticality"""
        return RiskEngine.ORGANIZATION_CRITICALITY_SCORES.get(criticality, 5)
    
    @staticmethod
    def get_district_sensitivity_score(district):
        """Get risk score for district sensitivity"""
        return RiskEngine.DISTRICT_SENSITIVITY.get(district, 4)
    
    @staticmethod
    def count_iocs(iocs_dict):
        """Count total indicators of compromise"""
        total = 0
        for key, values in iocs_dict.items():
            if isinstance(values, list):
                total += len(values)
        return total
    
    @staticmethod
    def get_ioc_score(ioc_count):
        """Convert IOC count to score"""
        if ioc_count >= 20:
            return 10
        elif ioc_count >= 10:
            return 8
        elif ioc_count >= 5:
            return 6
        elif ioc_count >= 2:
            return 4
        else:
            return 2
    
    @staticmethod
    def get_historical_incidents_score(organization, days=90):
        """Get score based on recent incidents against organization"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            count = db.threats.count_documents({
                "organizations": organization,
                "created_at": {"$gte": cutoff_date}
            })
            
            if count >= 10:
                return 10
            elif count >= 5:
                return 8
            elif count >= 2:
                return 5
            else:
                return 2
        except:
            return 2
    
    @staticmethod
    def calculate_risk_score(threat_analysis, organizations, districts):
        """
        Calculate overall risk score
        Returns score 0-10
        """
        try:
            scores = {}
            
            # Threat category score
            threat_category = threat_analysis.get("category", "Other")
            scores["threat_category"] = RiskEngine.get_threat_category_score(threat_category)
            
            # Organization criticality score
            if organizations:
                org_criticality_scores = []
                for org_id in organizations:
                    from models.protected_asset import ProtectedAsset
                    asset = ProtectedAsset.collection.find_one({"_id": org_id})
                    if asset:
                        crit = asset.get("criticality", "medium")
                        org_criticality_scores.append(
                            RiskEngine.get_organization_criticality_score(crit)
                        )
                scores["organization_criticality"] = max(org_criticality_scores) if org_criticality_scores else 5
            else:
                scores["organization_criticality"] = 3
            
            # District sensitivity score
            if districts:
                district_scores = [RiskEngine.get_district_sensitivity_score(d) for d in districts]
                scores["district_sensitivity"] = max(district_scores)
            else:
                scores["district_sensitivity"] = 2
            
            # IOC count score
            iocs = threat_analysis.get("indicators_of_compromise", {})
            ioc_count = RiskEngine.count_iocs(iocs)
            scores["ioc_count"] = RiskEngine.get_ioc_score(ioc_count)
            
            # Confidence score (already 0-10)
            confidence = threat_analysis.get("confidence", 50)
            scores["confidence"] = (confidence / 10)
            
            # Historical incidents score
            if organizations:
                hist_scores = []
                for org_id in organizations:
                    from models.protected_asset import ProtectedAsset
                    asset = ProtectedAsset.collection.find_one({"_id": org_id})
                    if asset:
                        hist_scores.append(
                            RiskEngine.get_historical_incidents_score(asset["name"])
                        )
                scores["historical_incidents"] = max(hist_scores) if hist_scores else 2
            else:
                scores["historical_incidents"] = 2
            
            # Calculate weighted score
            final_score = 0
            for factor, weight in RiskEngine.WEIGHTS.items():
                final_score += scores.get(factor, 0) * weight
            
            # Cap score at 10
            return min(round(final_score, 2), 10)
            
        except Exception as e:
            # Return moderate score on error
            return 5
    
    @staticmethod
    def calculate_alert_severity(risk_score):
        """Convert risk score to alert severity"""
        if risk_score >= 8:
            return "critical"
        elif risk_score >= 6:
            return "high"
        elif risk_score >= 4:
            return "medium"
        else:
            return "low"
