"""
Dynamic Risk Scorer Service for GeoShield AI
Calculates threat risk dynamically using multiple security factors
"""
from datetime import datetime, timedelta
from database.mongodb import db

class DynamicRiskScorer:
    """Calculates dynamic 0-100 risk score and maps to risk levels"""
    
    # Category severity mapping
    CATEGORY_SCORES = {
        "APT": 10.0,
        "Ransomware": 9.5,
        "Banking Malware": 9.0,
        "Data Breach": 8.5,
        "Fake APK": 8.0,
        "DDoS Attack": 7.5,
        "Credential Leak": 7.0,
        "Phishing": 6.0,
        "Identity Fraud": 6.0,
        "Money Laundering": 5.5,
        "Investment Scam": 5.0,
        "Cryptocurrency Scam": 5.0,
        "Malware": 7.0,
        "Other": 4.0
    }
    
    # Asset criticality mapping
    CRITICALITY_SCORES = {
        "critical": 10.0,
        "high": 8.0,
        "medium": 5.0,
        "low": 2.0
    }
    
    # District sensitivity mapping
    DISTRICT_SCORES = {
        "Bhopal": 10.0,
        "Indore": 9.0,
        "Jabalpur": 8.5,
        "Gwalior": 8.0,
        "Ujjain": 7.5,
        "Sagar": 6.5,
        "Ratlam": 5.5
    }
    
    @staticmethod
    def get_category_score(category):
        return DynamicRiskScorer.CATEGORY_SCORES.get(category, 4.0)
        
    @staticmethod
    def get_asset_criticality_score(matched_assets):
        if not matched_assets:
            return 3.0
        # Take the maximum criticality of all matched assets
        scores = [DynamicRiskScorer.CRITICALITY_SCORES.get(a.get("criticality", "medium").lower(), 5.0) for a in matched_assets]
        return max(scores)
        
    @staticmethod
    def get_district_score(districts):
        if not districts:
            return 3.0
        scores = [DynamicRiskScorer.DISTRICT_SCORES.get(d, 4.5) for d in districts]
        return max(scores)
        
    @staticmethod
    def get_ioc_score(iocs):
        if not iocs:
            return 1.0
        total_iocs = 0
        for key, values in iocs.items():
            if isinstance(values, list):
                total_iocs += len(values)
        
        if total_iocs >= 20:
            return 10.0
        elif total_iocs >= 10:
            return 8.0
        elif total_iocs >= 5:
            return 6.0
        elif total_iocs >= 2:
            return 4.0
        else:
            return 2.0
            
    @staticmethod
    def get_repeated_targeting_score(organizations, districts):
        """Check for repeated targets or districts in threat database over last 90 days"""
        try:
            cutoff = datetime.utcnow() - timedelta(days=90)
            
            # Count similar threats targeting these organizations or districts
            query_parts = []
            if organizations:
                query_parts.append({"organizations": {"$in": organizations}})
            if districts:
                query_parts.append({"districts": {"$in": districts}})
                
            if not query_parts:
                return 2.0
                
            query = {
                "created_at": {"$gte": cutoff},
                "$or": query_parts
            }
            
            count = db.threats.count_documents(query)
            if count >= 10:
                return 10.0
            elif count >= 5:
                return 8.0
            elif count >= 2:
                return 5.0
            else:
                return 2.0
        except Exception as e:
            return 2.0
            
    @staticmethod
    def get_historical_incidents_score(districts):
        """Check alert history in these districts in the last 90 days"""
        try:
            cutoff = datetime.utcnow() - timedelta(days=90)
            if not districts:
                return 2.0
                
            count = db.alerts.count_documents({
                "created_at": {"$gte": cutoff},
                "district": {"$in": districts}
            })
            
            if count >= 5:
                return 10.0
            elif count >= 3:
                return 8.0
            elif count >= 1:
                return 5.0
            else:
                return 2.0
        except Exception as e:
            return 2.0
            
    @staticmethod
    def calculate_score(analysis, matched_assets, districts, organizations):
        """
        Calculate overall 0-100 risk score and level.
        Returns: {
            "score": float, 
            "level": str, 
            "factors": dict
        }
        """
        category = analysis.get("threat_type", "Other")
        confidence = float(analysis.get("confidence", 50))
        iocs = analysis.get("indicators_of_compromise", {})
        
        # Calculate component scores (each 0-10)
        category_score = DynamicRiskScorer.get_category_score(category)
        asset_score = DynamicRiskScorer.get_asset_criticality_score(matched_assets)
        district_score = DynamicRiskScorer.get_district_score(districts)
        repeat_score = DynamicRiskScorer.get_repeated_targeting_score(organizations, districts)
        conf_score = confidence / 10.0
        ioc_score = DynamicRiskScorer.get_ioc_score(iocs)
        history_score = DynamicRiskScorer.get_historical_incidents_score(districts)
        
        # Weighted sum:
        # Category (20%) + Asset (20%) + District (15%) + Repeat Targeting (15%) + Confidence (10%) + IOC (10%) + History (10%)
        weighted_score = (
            (category_score * 0.20) +
            (asset_score * 0.20) +
            (district_score * 0.15) +
            (repeat_score * 0.15) +
            (conf_score * 0.10) +
            (ioc_score * 0.10) +
            (history_score * 0.10)
        )
        
        # Scale to 0-100
        final_score = min(100.0, max(0.0, round(weighted_score * 10, 1)))
        
        # Map to risk level
        if final_score >= 80:
            level = "critical"
        elif final_score >= 60:
            level = "high"
        elif final_score >= 40:
            level = "medium"
        else:
            level = "low"
            
        return {
            "score": final_score,
            "level": level,
            "breakdown": {
                "category": category_score,
                "asset": asset_score,
                "district": district_score,
                "repeat": repeat_score,
                "confidence": conf_score,
                "ioc": ioc_score,
                "history": history_score
            }
        }
