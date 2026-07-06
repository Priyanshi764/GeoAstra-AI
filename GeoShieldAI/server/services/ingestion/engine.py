"""
Threat Intelligence Ingestion Engine Core
"""
import time
from datetime import datetime
from database.mongodb import db
from ai.gemini_analyzer import GeminiAnalyzer
from ai.entity_mapper import EntityMapper
from ai.risk_engine import RiskEngine
from models.threat import Threat
from models.alert import Alert
from models.protected_asset import ProtectedAsset
from services.geofence_engine import GeofenceEngine
from services.socket_service import SocketService
from services.ingestion.connectors import (
    URLHausConnector, PhishTankConnector, RSSConnector,
    NVDConnector, CISAConnector
)

class IngestionEngine:
    def __init__(self):
        self.connectors = [
            URLHausConnector(),
            PhishTankConnector(),
            RSSConnector(),
            NVDConnector(),
            CISAConnector()
        ]
        self.collection = db.ingested_intelligence
        print("[INGESTION] Engine initialized.")

    def run_cycle(self):
        """Run one complete ingestion cycle"""
        print(f"\n[INGESTION] Starting cycle at {datetime.utcnow().isoformat()}")
        
        for connector in self.connectors:
            print(f"[INGESTION] Running connector: {connector.name}")
            try:
                items = connector.fetch()
                new_items = self._filter_new_items(items)
                
                if not new_items:
                    print(f"[INGESTION] No new items from {connector.name}")
                    continue
                    
                print(f"[INGESTION] Found {len(new_items)} new items from {connector.name}")
                
                for item in new_items:
                    success = self._process_item(item)
                    if success:
                        self._mark_as_processed(item['id'])
                        
            except Exception as e:
                print(f"[INGESTION] Error running {connector.name}: {str(e)}")
                
        print("[INGESTION] Cycle completed.\n")

    def _filter_new_items(self, items):
        """Filter out items that have already been processed"""
        if not items:
            return []
            
        item_ids = [item['id'] for item in items]
        
        # Find which ones exist in DB
        existing = list(self.collection.find({"_id": {"$in": item_ids}}, {"_id": 1}))
        existing_ids = set([doc['_id'] for doc in existing])
        
        return [item for item in items if item['id'] not in existing_ids]

    def _mark_as_processed(self, item_id):
        """Mark an item as processed in the database"""
        self.collection.insert_one({
            "_id": item_id,
            "processed_at": datetime.utcnow()
        })

    def _process_item(self, item):
        """Process a single threat intelligence item through the AI pipeline"""
        try:
            print(f"[INGESTION] Processing item: {item['id']}")
            text_content = item['text']
            source_name = f"Ingestion_{item['source']}"
            
            # 1. Analyze with Gemini
            analysis_result = GeminiAnalyzer.analyze_intelligence(text_content)
            if not analysis_result.get('success'):
                print(f"[INGESTION] AI Analysis failed for {item['id']}")
                return False
                
            analysis = analysis_result['analysis']
            
            # 2. Extract entities
            org_result = GeminiAnalyzer.extract_organizations(text_content)
            loc_result = GeminiAnalyzer.extract_locations(text_content)
            
            organizations = org_result.get('organizations', [])
            locations = loc_result.get('locations', [])
            
            # 3. Map entities
            mapping = EntityMapper.map_intelligence(locations, organizations)
            
            # 4. Match assets
            matched_assets = list(ProtectedAsset.collection.find({
                "name": {"$in": organizations}
            }))
            asset_ids = [str(asset['_id']) for asset in matched_assets]
            
            # 5. Calculate risk
            risk_score = RiskEngine.calculate_risk_score(analysis, asset_ids, mapping['districts'])
            alert_severity = RiskEngine.calculate_alert_severity(risk_score)
            
            # 6. Create Threat
            threat_data = {
                "source": source_name,
                "threat_type": analysis.get("threat_type", "Unknown"),
                "category": analysis.get("category", "Other"),
                "risk_score": risk_score,
                "confidence": analysis.get("confidence", 0),
                "summary": analysis.get("summary", ""),
                "recommendation": analysis.get("recommendation", ""),
                "mitre_attack": analysis.get("mitre_attack", []),
                "organizations": organizations,
                "districts": mapping['districts'],
                "state": "Madhya Pradesh",
                "threat_actors": analysis.get("threat_actors", []),
                "attack_vector": analysis.get("attack_vector", ""),
                "malware_family": analysis.get("malware_family", ""),
                "iocs": analysis.get("indicators_of_compromise", {}),
                "created_by": "system"
            }
            
            threat_result = Threat.create_threat(threat_data)
            if not threat_result.get('success'):
                print(f"[INGESTION] Failed to create threat record for {item['id']}")
                return False
                
            threat_id = threat_result['threat_id']
            
            # 7. Create Alerts
            for asset in mapping['assets']:
                alert_data = {
                    "threat_id": threat_id,
                    "title": f"New {analysis.get('threat_type', 'Security')} Threat Detected",
                    "description": analysis.get("summary", ""),
                    "severity": alert_severity,
                    "category": analysis.get("category", ""),
                    "organization": asset['asset_name'],
                    "district": asset['district'],
                    "affected_assets": [asset['asset_id']],
                    "recommended_action": analysis.get("recommendation", "")
                }
                Alert.create_alert(alert_data)
                
            # 8. Trigger Geofence Engine
            GeofenceEngine.process_threat(threat_id, analysis, organizations, mapping['districts'], text_content)
            
            # Note: Socket event is emitted by GeofenceEngine.process_threat ("geofence_triggered" and "dashboard_refresh").
            # However, we can also emit a 'new_threat' event if needed.
            # Let's emit a general intelligence update
            SocketService.broadcast_event("intelligence_ingested", {
                "source": source_name,
                "threat_id": threat_id,
                "summary": analysis.get("summary", "")
            })
            
            return True
            
        except Exception as e:
            print(f"[INGESTION] Error processing item {item.get('id', 'unknown')}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
