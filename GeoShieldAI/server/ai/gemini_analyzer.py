"""
Gemini AI Integration for GeoShield AI
Analyzes threat intelligence using Google's Gemini API
Falls back to offline analyzer when API is unavailable
"""
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from ai.offline_analyzer import OfflineAnalyzer

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiAnalyzer:
    """Analyzes threat intelligence using Gemini API with offline fallback"""
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    @staticmethod
    def get_offline_analysis(text_content):
        """Use offline analyzer when Gemini is unavailable"""
        return OfflineAnalyzer.analyze(text_content)
    
    @staticmethod
    def analyze_intelligence(text_content):
        """
        Analyze threat intelligence using Gemini or offline analyzer
        Returns structured threat analysis
        """
        try:
            prompt = """You are a cybersecurity expert analyzing threat intelligence. Analyze the following intelligence report and provide a structured JSON response.

Intelligence Report:
""" + text_content + """

Provide a detailed JSON analysis with the following structure (return ONLY valid JSON, no markdown):
{
    "threat_type": "Type of threat like Malware or Phishing",
    "category": "Category like APT or Cybercrime",
    "risk_score": 7,
    "confidence": 85,
    "summary": "Brief summary of the threat",
    "recommendation": "Recommended response",
    "mitre_attack": ["T1021", "T1566"],
    "threat_actors": ["Threat actor name"],
    "attack_vector": "Primary attack vector",
    "malware_family": "Malware family if known",
    "indicators_of_compromise": {
        "domains": [],
        "ips": [],
        "urls": [],
        "emails": [],
        "hashes": [],
        "telegram_handles": [],
        "phone_numbers": [],
        "crypto_wallets": []
    },
    "affected_sectors": [],
    "notes": "Additional notes"
}
Return ONLY JSON, no extra text."""
            
            response = GeminiAnalyzer.model.generate_content(prompt)
            
            # Parse JSON from response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            return {"success": True, "analysis": analysis}
            
        except Exception as e:
            # If API quota exceeded or error, use offline analyzer
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str or "generativeai" in error_str:
                print(f"[OFFLINE MODE] Gemini API unavailable, using offline analyzer")
                analysis = GeminiAnalyzer.get_offline_analysis(text_content)
                return {"success": True, "analysis": analysis}
            
            # For any other error, also fallback to offline
            print(f"[OFFLINE MODE] Gemini analysis failed: {str(e)}, using offline analyzer")
            analysis = GeminiAnalyzer.get_offline_analysis(text_content)
            return {"success": True, "analysis": analysis}
    
    @staticmethod
    def extract_organizations(text_content):
        """Extract organization names from threat intelligence"""
        try:
            prompt = f"""
From the following threat intelligence, extract all organization/company names that are mentioned or could be targeted.
Intelligence:
{text_content}

Return a JSON array of organization names only. Example: {{"organizations": ["Company A", "Company B"]}}
Return ONLY valid JSON.
"""
            
            response = GeminiAnalyzer.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            data = json.loads(response_text)
            return {"success": True, "organizations": data.get("organizations", [])}
            
        except Exception as e:
            # Use offline analyzer
            organizations = OfflineAnalyzer.extract_organizations(text_content)
            return {"success": True, "organizations": organizations}
    
    @staticmethod
    def extract_locations(text_content):
        """Extract location mentions from threat intelligence"""
        try:
            prompt = f"""
From the following threat intelligence, extract all geographic locations, cities, and districts mentioned.
Intelligence:
{text_content}

Return a JSON array of locations. Example: {{"locations": ["Bhopal", "Indore", "Jabalpur"]}}
Return ONLY valid JSON.
"""
            
            response = GeminiAnalyzer.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            data = json.loads(response_text)
            return {"success": True, "locations": data.get("locations", [])}
            
        except Exception as e:
            # Use offline analyzer
            locations = OfflineAnalyzer.extract_locations(text_content)
            return {"success": True, "locations": locations}
    
    @staticmethod
    def summarize_intelligence(text_content):
        """Generate an executive summary of threat intelligence"""
        try:
            prompt = f"""
Generate a concise executive summary (2-3 sentences) of this threat intelligence:
{text_content}

Summary:
"""
            
            response = GeminiAnalyzer.model.generate_content(prompt)
            return {
                "success": True,
                "summary": response.text.strip()
            }
            
        except Exception as e:
            # Use offline analyzer
            threat_type, _ = OfflineAnalyzer.extract_threat_type(text_content)
            organizations = OfflineAnalyzer.extract_organizations(text_content)
            iocs = OfflineAnalyzer.extract_iocs(text_content)
            ioc_count = sum(len(v) for v in iocs.values() if isinstance(v, list))
            
            summary = OfflineAnalyzer.generate_summary(text_content, threat_type, organizations, ioc_count)
            return {
                "success": True,
                "summary": summary
            }

