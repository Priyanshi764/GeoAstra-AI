"""
Entity Mapper for GeoShield AI
Maps extracted entities to Madhya Pradesh districts and protected assets
"""
import json
from fuzzywuzzy import fuzz
from models.protected_asset import ProtectedAsset

# Madhya Pradesh districts
MP_DISTRICTS = [
    "Indore", "Bhopal", "Jabalpur", "Nagpur", "Gwalior",
    "Ujjain", "Sagar", "Ratlam", "Morena", "Shivpuri",
    "Itarsi", "Vidisha", "Chhindwara", "Seoni", "Mandla",
    "Narmadapuram", "Raisen", "Katni", "Satna", "Rewa",
    "Khajuraho", "Shahdol", "Umaria", "Anuppur", "Balaghat",
    "Dindori", "Betul", "Khandwa", "Khandwasan", "Badwani",
    "Ashoknagar", "Niwari", "Chhatarpur", "Damoh", "Panna"
]

class EntityMapper:
    """Maps entities to locations and assets"""
    
    @staticmethod
    def match_district(location_text):
        """
        Match location text to Madhya Pradesh districts
        Returns matched district and confidence score
        """
        best_match = None
        best_score = 0
        
        for district in MP_DISTRICTS:
            score = fuzz.ratio(location_text.lower(), district.lower())
            if score > best_score:
                best_score = score
                best_match = district
        
        # Return if match confidence is above 70%
        if best_score >= 70:
            return {"district": best_match, "confidence": best_score}
        return None
    
    @staticmethod
    def match_assets(organization_names):
        """
        Match organization names to protected assets
        Returns list of matched assets
        """
        matched_assets = []
        
        all_assets = ProtectedAsset.get_all_assets()
        
        for org_name in organization_names:
            for asset in all_assets:
                score = fuzz.ratio(org_name.lower(), asset["name"].lower())
                if score >= 70:
                    matched_assets.append({
                        "asset_id": asset["_id"],
                        "asset_name": asset["name"],
                        "type": asset["type"],
                        "district": asset["district"],
                        "match_score": score
                    })
        
        return matched_assets
    
    @staticmethod
    def map_intelligence(locations, organizations):
        """
        Map extracted locations and organizations
        Returns mapped districts and assets
        """
        result = {
            "districts": [],
            "assets": [],
            "unmatched_locations": [],
            "unmatched_organizations": []
        }
        
        # Map locations to districts
        for location in locations:
            match = EntityMapper.match_district(location)
            if match:
                if match["district"] not in result["districts"]:
                    result["districts"].append(match["district"])
            else:
                result["unmatched_locations"].append(location)
        
        # Map organizations to assets
        matched_assets = EntityMapper.match_assets(organizations)
        for asset in matched_assets:
            if asset not in result["assets"]:
                result["assets"].append(asset)
        
        # Record unmatched organizations
        matched_org_names = [asset["asset_name"] for asset in matched_assets]
        for org in organizations:
            if org not in matched_org_names:
                result["unmatched_organizations"].append(org)
        
        return result
