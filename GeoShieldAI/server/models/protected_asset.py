"""
Protected Asset Model for GeoShield AI
Manages critical infrastructure and protected assets database
"""
from datetime import datetime
from bson.objectid import ObjectId
from database.mongodb import db

class ProtectedAsset:
    """Model for managing protected assets and critical infrastructure"""
    
    collection = db.protected_assets
    
    @staticmethod
    def create_asset(asset_data):
        """Create a new protected asset"""
        try:
            asset_record = {
                "name": asset_data.get("name", ""),
                "type": asset_data.get("type", ""),  # Bank, Government, University, Hospital, Police, Municipal
                "district": asset_data.get("district", ""),
                "state": asset_data.get("state", "Madhya Pradesh"),
                "address": asset_data.get("address", ""),
                "latitude": asset_data.get("latitude", None),
                "longitude": asset_data.get("longitude", None),
                "criticality": asset_data.get("criticality", "high"),  # low, medium, high, critical
                "sectors": asset_data.get("sectors", []),
                "contact_email": asset_data.get("contact_email", ""),
                "contact_phone": asset_data.get("contact_phone", ""),
                "description": asset_data.get("description", ""),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_active": True
            }
            
            result = ProtectedAsset.collection.insert_one(asset_record)
            return {
                "success": True,
                "asset_id": str(result.inserted_id),
                "message": "Asset created successfully"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def get_all_assets():
        """Get all protected assets"""
        try:
            assets = list(ProtectedAsset.collection.find({"is_active": True}))
            for asset in assets:
                asset["_id"] = str(asset["_id"])
            return assets
        except Exception as e:
            return []
    
    @staticmethod
    def get_assets_by_district(district):
        """Get assets in a specific district"""
        try:
            assets = list(ProtectedAsset.collection.find({
                "district": district,
                "is_active": True
            }))
            for asset in assets:
                asset["_id"] = str(asset["_id"])
            return assets
        except Exception as e:
            return []
    
    @staticmethod
    def get_assets_by_type(asset_type):
        """Get assets by type"""
        try:
            assets = list(ProtectedAsset.collection.find({
                "type": asset_type,
                "is_active": True
            }))
            for asset in assets:
                asset["_id"] = str(asset["_id"])
            return assets
        except Exception as e:
            return []
    
    @staticmethod
    def search_assets(query):
        """Search assets by name or address"""
        try:
            assets = list(ProtectedAsset.collection.find({
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"address": {"$regex": query, "$options": "i"}}
                ],
                "is_active": True
            }))
            for asset in assets:
                asset["_id"] = str(asset["_id"])
            return assets
        except Exception as e:
            return []
    
    @staticmethod
    def get_critical_assets():
        """Get all critical assets"""
        try:
            assets = list(ProtectedAsset.collection.find({
                "criticality": {"$in": ["critical", "high"]},
                "is_active": True
            }))
            for asset in assets:
                asset["_id"] = str(asset["_id"])
            return assets
        except Exception as e:
            return []
