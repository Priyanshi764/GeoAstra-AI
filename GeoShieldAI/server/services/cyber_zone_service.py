"""
Cyber Zone Service for GeoShield AI
Coordinates cyber zone status calculations and updates
"""
from models.cyber_zone import CyberZone
from models.protected_asset import ProtectedAsset
from models.threat import Threat
from models.geofence_alert import GeofenceAlert
from database.mongodb import db

MP_DISTRICTS = [
    "Jabalpur", "Bhopal", "Indore", "Gwalior", "Ujjain",
    "Sagar", "Ratlam", "Morena", "Shivpuri", "Vidisha",
    "Chhindwara", "Seoni", "Mandla", "Rewa", "Khajuraho", "Balaghat"
]

class CyberZoneService:
    """Service to query and update Cyber Zone statistics"""
    
    @staticmethod
    def get_zone_status(district):
        """Aggregate stats for a specific Cyber Zone (district)"""
        try:
            # 1. Get protected assets in this district
            assets = ProtectedAsset.get_assets_by_district(district)
            asset_count = len(assets)
            
            # 2. Get threat count
            threat_count = db.threats.count_documents({"districts": district})
            
            # 3. Get active incident count (unresolved alerts)
            active_incidents = db.geofence_alerts.count_documents({
                "district": district,
                "status": {"$ne": "resolved"}
            })
            
            # 4. Calculate dynamic risk from recent threats
            recent_threats = list(db.threats.find({"districts": district}).sort("created_at", -1).limit(10))
            if recent_threats:
                # Average of recent risk scores (or max if preferred for safety)
                total_risk = sum(t.get("risk_score", 0) for t in recent_threats)
                # Map 0-10 existing risk scores to 0-100 scale if stored as 0-10
                avg_risk = total_risk / len(recent_threats)
                # Check if it is stored as 0-10 or 0-100
                if avg_risk <= 10.0:
                    avg_risk = avg_risk * 10.0
                risk_score = round(avg_risk, 1)
            else:
                risk_score = 0.0
                
            # Determine risk level
            if risk_score >= 80:
                risk_level = "critical"
            elif risk_score >= 60:
                risk_level = "high"
            elif risk_score >= 40:
                risk_level = "medium"
            else:
                risk_level = "low"
                
            # Save stats to CyberZone collection
            CyberZone.update_zone_stats(
                district=district,
                risk_score=risk_score,
                risk_level=risk_level,
                threat_count=threat_count,
                active_incidents=active_incidents
            )
            
            return {
                "district": district,
                "zone_name": f"{district} Cyber Zone",
                "asset_count": asset_count,
                "threat_count": threat_count,
                "active_incidents": active_incidents,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "protected_assets": assets
            }
        except Exception as e:
            return {
                "district": district,
                "zone_name": f"{district} Cyber Zone",
                "asset_count": 0,
                "threat_count": 0,
                "active_incidents": 0,
                "risk_score": 0.0,
                "risk_level": "low",
                "protected_assets": []
            }
            
    @staticmethod
    def get_all_zones():
        """Retrieve aggregated stats for all MP Cyber Zones using cached DB stats and batch queries"""
        try:
            # 1. Fetch all zones from cyber_zones collection
            db_zones = {z["district"]: z for z in CyberZone.get_all_zones()}
            
            # 2. Fetch all active protected assets and group by district in memory
            all_assets = list(db.protected_assets.find({"is_active": True}))
            assets_by_district = {}
            for asset in all_assets:
                asset["_id"] = str(asset["_id"])
                dist = asset.get("district")
                if dist:
                    if dist not in assets_by_district:
                        assets_by_district[dist] = []
                    assets_by_district[dist].append(asset)
            
            zones_data = []
            for district in MP_DISTRICTS:
                zone = db_zones.get(district)
                if not zone:
                    # If zone is not in DB, calculate dynamically to initialize it in DB
                    status = CyberZoneService.get_zone_status(district)
                    # Attach the up-to-date dynamic assets
                    status["protected_assets"] = assets_by_district.get(district, [])
                    status["asset_count"] = len(status["protected_assets"])
                    zones_data.append(status)
                else:
                    district_assets = assets_by_district.get(district, [])
                    zones_data.append({
                        "district": district,
                        "zone_name": zone.get("zone_name", f"{district} Cyber Zone"),
                        "asset_count": len(district_assets),
                        "threat_count": zone.get("threat_count", 0),
                        "active_incidents": zone.get("active_incidents", 0),
                        "risk_score": zone.get("risk_score", 0.0),
                        "risk_level": zone.get("risk_level", "low"),
                        "protected_assets": district_assets
                    })
                    
            return sorted(zones_data, key=lambda x: x["risk_score"], reverse=True)
        except Exception as e:
            print(f"Error in get_all_zones optimized: {e}")
            # Fallback to dynamic loop if db query fails
            zones_data = []
            for district in MP_DISTRICTS:
                status = CyberZoneService.get_zone_status(district)
                zones_data.append(status)
            return sorted(zones_data, key=lambda x: x["risk_score"], reverse=True)
        
    @staticmethod
    def update_zone_on_trigger(district, threat_risk_score, risk_level):
        """Called by GeofenceEngine to incrementally bump stats when a new threat lands"""
        try:
            # Re-aggregate to ensure correctness
            CyberZoneService.get_zone_status(district)
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
