"""
Asset Matcher Service for GeoShield AI
Matches extracted intelligence organizations and locations to protected assets
"""
from fuzzywuzzy import fuzz
from models.protected_asset import ProtectedAsset

class AssetMatcher:
    """Matches threat intelligence entities to the Protected Asset Registry"""
    
    @staticmethod
    def match_assets(organizations, districts, raw_text=""):
        """
        Match extracted organizations and districts to Protected Assets.
        If raw_text is provided, perform additional keyword searches.
        """
        matched = []
        all_assets = ProtectedAsset.get_all_assets()
        
        # Lowercase everything for comparison
        orgs_lower = [org.lower().strip() for org in organizations if org]
        districts_lower = [dist.lower().strip() for dist in districts if dist]
        raw_text_lower = raw_text.lower() if raw_text else ""
        
        for asset in all_assets:
            asset_name = asset["name"].lower()
            asset_district = asset["district"].lower()
            asset_type = asset["type"].lower()
            
            is_org_match = False
            match_score = 0
            match_reason = ""
            
            # 1. Exact or Substring organization matching
            for org in orgs_lower:
                if org == "general" or org == "unknown":
                    continue
                # If extracted org is a substring of the asset name (e.g., "sbi" in "sbi regional office")
                # or vice-versa (e.g., "sbi regional office" in "selling fake sbi apk...")
                if org in asset_name or asset_name in org:
                    is_org_match = True
                    match_score = 100
                    match_reason = f"Organization match: '{org}' in asset name '{asset['name']}'"
                    break
                    
                # Fuzzy matching
                ratio = fuzz.ratio(org, asset_name)
                partial_ratio = fuzz.partial_ratio(org, asset_name)
                best_ratio = max(ratio, partial_ratio)
                
                if best_ratio >= 75:
                    is_org_match = True
                    match_score = best_ratio
                    match_reason = f"Fuzzy organization match: '{org}' and '{asset['name']}' ({best_ratio}%)"
                    break
            
            # 2. Raw text keyword check (fallback or additional verification)
            if not is_org_match and raw_text_lower:
                # Direct check if asset name keywords exist in raw text
                # Tokenize asset name to avoid short word false positives
                keywords = [w for w in asset_name.replace(",", " ").split() if len(w) > 3 or w in ["sbi", "iit", "nit"]]
                if keywords and all(kw in raw_text_lower for kw in keywords):
                    is_org_match = True
                    match_score = 90
                    match_reason = f"Asset name keywords found in raw threat intelligence"
            
            # 3. District matching
            is_district_match = False
            if districts_lower:
                if asset_district in districts_lower:
                    is_district_match = True
            elif raw_text_lower:
                # If no district extracted but district name is in text
                if asset_district in raw_text_lower:
                    is_district_match = True
            
            # Decide on match:
            # If organization matches, and district matches (if district is mentioned)
            if is_org_match:
                final_score = match_score
                # Boost score if district also matches
                if is_district_match:
                    final_score = min(100, final_score + 15)
                    match_reason += " (District matched)"
                elif districts_lower:
                    # If districts were specified but this asset is in a different district,
                    # decrease score or don't match if it's a district-specific search
                    final_score = max(50, final_score - 20)
                    match_reason += " (District mismatch)"
                    
                matched.append({
                    "asset_id": asset["_id"],
                    "asset_name": asset["name"],
                    "type": asset["type"],
                    "district": asset["district"],
                    "criticality": asset.get("criticality", "medium"),
                    "match_score": final_score,
                    "match_reason": match_reason,
                    "is_district_match": is_district_match
                })
            elif is_district_match and asset.get("criticality") == "critical" and any(k in raw_text_lower for k in [asset_type, asset_name]):
                # If district matches and it is critical asset and type is mentioned (e.g. "hospital" or "bank" in Jabalpur)
                matched.append({
                    "asset_id": asset["_id"],
                    "asset_name": asset["name"],
                    "type": asset["type"],
                    "district": asset["district"],
                    "criticality": asset.get("criticality", "medium"),
                    "match_score": 80,
                    "match_reason": f"Critical asset type match in target district '{asset['district']}'",
                    "is_district_match": True
                })
                
        # Sort matched assets by match score descending
        matched = sorted(matched, key=lambda x: x["match_score"], reverse=True)
        return matched
