"""
Offline Threat Analysis Engine for GeoShield AI
Production-quality threat intelligence analysis without external APIs
Uses regex, NLP, keyword matching, and heuristics for dynamic analysis
"""

import re
import json
from collections import Counter

class OfflineAnalyzer:
    """Production-grade offline threat analysis engine"""
    
    # Threat type keywords and patterns
    THREAT_PATTERNS = {
        "Banking Malware": {
            "keywords": ["banking", "apk", "otp", "credentials", "steals", "malware", "trojan", "banking app", "payment app"],
            "patterns": [r"banking\s+(?:app|malware)", r"(?:otp|credential).*(?:steal|hijack)", r"fake.*(?:bank|payment)"],
            "weight": 0.95
        },
        "Phishing": {
            "keywords": ["phishing", "spoof", "impersonat", "fake email", "credential harvesting", "login page", "verify account"],
            "patterns": [r"phishing", r"spoof(?:ing)?", r"impersonat.*(?:email|form)", r"credential\s+harvest"],
            "weight": 0.90
        },
        "Fake APK": {
            "keywords": ["apk", "fake", "android", "app", "clone", "trojan", "malicious app"],
            "patterns": [r"fake\s+(?:apk|app)", r"(?:apk|android)\s+.*(?:malware|trojan)", r"(?:phoney|clone).*(?:app|apk)"],
            "weight": 0.85
        },
        "Credential Leak": {
            "keywords": ["credential leak", "leaked", "compromised", "dump", "database", "employees", "users"],
            "patterns": [r"(?:leaked|compromised).*(?:credential|password|user)", r"credential.*(?:leak|dump)", r"database.*(?:stolen|leaked)"],
            "weight": 0.88
        },
        "Ransomware": {
            "keywords": ["ransomware", "encryption", "ransom", "lock", "payload", "encryptor"],
            "patterns": [r"ransomware", r"(?:encrypted|locked).*(?:file|system)", r"ransom.*(?:demand|payment)"],
            "weight": 0.92
        },
        "Data Breach": {
            "keywords": ["data breach", "data theft", "stolen data", "exfiltration", "breach"],
            "patterns": [r"data.*(?:breach|theft)", r"(?:stolen|exfiltrated).*(?:data|database|records)"],
            "weight": 0.87
        },
        "Investment Scam": {
            "keywords": ["investment scam", "fake investment", "fraud", "scheme", "ponzi"],
            "patterns": [r"(?:investment|financial).*(?:scam|fraud)", r"fake.*(?:investment|opportunity)"],
            "weight": 0.82
        },
        "Identity Fraud": {
            "keywords": ["identity fraud", "fake documents", "aadhaar", "pan", "forged", "fraud"],
            "patterns": [r"(?:fake|forged).*(?:document|aadhaar|pan)", r"identity.*(?:fraud|theft)"],
            "weight": 0.85
        },
        "Money Laundering": {
            "keywords": ["money launder", "mule account", "fund transfer", "black money", "layering"],
            "patterns": [r"(?:money|fund).*(?:launder|clean)", r"mule.*(?:account|recruitment)"],
            "weight": 0.83
        },
        "Cryptocurrency Scam": {
            "keywords": ["crypto scam", "bitcoin scam", "ethereum", "wallet", "fake crypto"],
            "patterns": [r"(?:crypto|bitcoin|ethereum).*(?:scam|fraud)", r"fake.*(?:crypto|cryptocurrency)"],
            "weight": 0.81
        },
        "DDoS Attack": {
            "keywords": ["ddos", "dos attack", "botnet", "flood", "attack", "offline"],
            "patterns": [r"(?:ddos|dos).*(?:attack|campaign)", r"botnet", r"(?:flood|attack).*(?:server|service)"],
            "weight": 0.84
        },
        "Malware": {
            "keywords": ["malware", "virus", "trojan", "worm", "spyware", "backdoor"],
            "patterns": [r"malware", r"(?:virus|trojan|worm|spyware|backdoor)"],
            "weight": 0.86
        }
    }
    
    # IOC extraction patterns
    IOC_PATTERNS = {
        "urls": r"(?:https?://)?(?:www\.)?[a-zA-Z0-9\-\.]+\.[a-z]{2,}(?:/[^\s]*)?",
        "domains": r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}",
        "emails": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "ips": r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
        "telegram": r"@[a-zA-Z0-9_]{4,32}",
        "bitcoin": r"(?:bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}",
        "ethereum": r"0x[a-fA-F0-9]{40}",
        "md5": r"\b[a-fA-F0-9]{32}\b",
        "sha256": r"\b[a-fA-F0-9]{64}\b",
        "phone": r"(?:\+91|0)?[6-9]\d{9}",
        "apk_package": r"(?:com|org|net)\.[a-zA-Z0-9][a-zA-Z0-9.]*"
    }
    
    # MITRE ATT&CK mapping
    MITRE_MAPPING = {
        "Banking Malware": ["T1566.002", "T1566.001", "T1005", "T1041"],
        "Phishing": ["T1566.002", "T1566.001", "T1598.003"],
        "Fake APK": ["T1444", "T1444.1", "T1566.002"],
        "Credential Leak": ["T1589.001", "T1040"],
        "Ransomware": ["T1486", "T1565.001"],
        "Data Breach": ["T1020", "T1041", "T1030"],
        "Investment Scam": ["T1598.003", "T1598.004"],
        "Identity Fraud": ["T1589.001"],
        "Money Laundering": ["T1020"],
        "Cryptocurrency Scam": ["T1598.003"],
        "DDoS Attack": ["T1498", "T1498.1"],
        "Malware": ["T1204.002", "T1204.001"]
    }
    
    # Attack vectors
    ATTACK_VECTORS = {
        "email": ["email", "phishing", "spear phishing", "credential"],
        "web": ["website", "web", "browser", "exploit", "watering hole"],
        "social": ["social media", "telegram", "whatsapp", "facebook", "twitter"],
        "mobile": ["apk", "app", "mobile", "android"],
        "network": ["network", "lan", "vpn", "firewall", "ddos"],
        "physical": ["usb", "device", "hardware", "physical"]
    }
    
    @staticmethod
    def extract_threat_type(text):
        """Dynamically classify threat type based on content"""
        text_lower = text.lower()
        threat_scores = {}
        
        for threat_type, config in OfflineAnalyzer.THREAT_PATTERNS.items():
            score = 0
            keyword_matches = sum(1 for keyword in config["keywords"] if keyword in text_lower)
            if keyword_matches > 0:
                score += (keyword_matches / len(config["keywords"])) * 0.6
            
            pattern_matches = sum(1 for pattern in config["patterns"] if re.search(pattern, text_lower, re.IGNORECASE))
            if pattern_matches > 0:
                score += (pattern_matches / len(config["patterns"])) * 0.4
            
            if score > 0:
                threat_scores[threat_type] = min(score * config["weight"], 1.0)
        
        if threat_scores:
            threat_type = max(threat_scores, key=threat_scores.get)
            confidence = int(threat_scores[threat_type] * 100)
            return threat_type, confidence
        return "Malware", 45
    
    @staticmethod
    def extract_organizations(text):
        """Extract organization names from text"""
        text_lower = text.lower()
        organizations = set()
        
        org_keywords = {
            "banks": ["sbi", "hdfc", "icici", "axis", "bank"],
            "hospitals": ["aiims", "hospital"],
            "universities": ["iit", "nit", "university", "college", "iiitdm", "rani durgavati"],
            "government": ["government", "collectorate", "police", "municipality", "municipal corporation"],
            "companies": ["phoned", "google pay", "paytm", "industry"]
        }
        
        for category, keywords in org_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    pattern = r"(?:the\s+)?(\w+(?:\s+\w+)*?\s+" + re.escape(keyword) + r")"
                    matches = re.findall(pattern, text_lower, re.IGNORECASE)
                    if matches:
                        for match in matches:
                            org_name = match.strip().title()
                            if len(org_name) > 2:
                                organizations.add(org_name)
                    else:
                        organizations.add(keyword.title())
        
        if not organizations:
            words = text.split()
            for word in words:
                if word and word[0].isupper() and len(word) > 3:
                    if any(org_word in word.lower() for org_word in ["organization", "company", "bank", "office", "center"]):
                        organizations.add(word)
        
        return list(organizations) if organizations else ["General"]
    
    @staticmethod
    def extract_locations(text):
        """Extract geographic locations from text"""
        text_lower = text.lower()
        locations = set()
        
        districts = [
            "indore", "bhopal", "jabalpur", "nagpur", "gwalior", "ujjain",
            "sagar", "ratlam", "morena", "shivpuri", "vidisha", "chhindwara",
            "seoni", "mandla", "rewa", "khajuraho", "balaghat"
        ]
        
        for district in districts:
            if district in text_lower:
                locations.add(district.title())
        
        return list(locations) if locations else ["Unknown"]
    
    @staticmethod
    def extract_iocs(text):
        """Extract all indicators of compromise"""
        iocs = {
            "urls": [],
            "domains": [],
            "ips": [],
            "emails": [],
            "telegram_handles": [],
            "phone_numbers": [],
            "crypto_wallets": [],
            "apk_packages": [],
            "hashes": []
        }
        
        urls = re.findall(OfflineAnalyzer.IOC_PATTERNS["urls"], text)
        iocs["urls"] = list(set(urls))[:10]
        
        domains = re.findall(OfflineAnalyzer.IOC_PATTERNS["domains"], text)
        iocs["domains"] = list(set(domains))[:10]
        
        emails = re.findall(OfflineAnalyzer.IOC_PATTERNS["emails"], text)
        iocs["emails"] = list(set(emails))[:10]
        
        ips = re.findall(OfflineAnalyzer.IOC_PATTERNS["ips"], text)
        iocs["ips"] = list(set(ips))[:10]
        
        telegrams = re.findall(OfflineAnalyzer.IOC_PATTERNS["telegram"], text)
        iocs["telegram_handles"] = list(set(telegrams))[:5]
        
        bitcoins = re.findall(OfflineAnalyzer.IOC_PATTERNS["bitcoin"], text)
        ethereums = re.findall(OfflineAnalyzer.IOC_PATTERNS["ethereum"], text)
        iocs["crypto_wallets"] = list(set(bitcoins + ethereums))[:5]
        
        apks = re.findall(OfflineAnalyzer.IOC_PATTERNS["apk_package"], text)
        iocs["apk_packages"] = list(set(apks))[:5]
        
        sha256 = re.findall(OfflineAnalyzer.IOC_PATTERNS["sha256"], text)
        md5 = re.findall(OfflineAnalyzer.IOC_PATTERNS["md5"], text)
        iocs["hashes"] = list(set(sha256 + md5))[:10]
        
        return iocs
    
    @staticmethod
    def detect_attack_vector(text):
        """Detect primary attack vector"""
        text_lower = text.lower()
        vector_scores = {}
        
        for vector, keywords in OfflineAnalyzer.ATTACK_VECTORS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                vector_scores[vector] = score
        
        if vector_scores:
            return max(vector_scores, key=vector_scores.get).title()
        return "Network"
    
    @staticmethod
    def generate_summary(text, threat_type, organizations, ioc_count):
        """Generate dynamic summary"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        summary_parts = []
        summary_parts.append(f"Intelligence report identifies a {threat_type.lower()} threat")
        
        if organizations and organizations != ["General"]:
            org_str = ", ".join(organizations[:2])
            summary_parts.append(f"targeting {org_str}")
        
        if ioc_count > 5:
            summary_parts.append(f"with {ioc_count} indicators of compromise identified")
        elif ioc_count > 0:
            summary_parts.append(f"with {ioc_count} IOC(s) detected")
        
        if sentences:
            important = sentences[0]
            if len(important) > 100:
                important = important[:100] + "..."
            summary_parts.append(f"Details: {important}")
        
        return ". ".join(summary_parts) + "."
    
    @staticmethod
    def generate_recommendations(threat_type, attack_vector, ioc_count):
        """Generate dynamic recommendations"""
        recommendations = []
        
        if threat_type == "Phishing":
            recommendations.extend([
                "Implement advanced email filtering and authentication",
                "Conduct user security awareness training",
                "Enable multi-factor authentication on critical accounts"
            ])
        elif threat_type == "Banking Malware":
            recommendations.extend([
                "Deploy endpoint detection and response (EDR) solutions",
                "Block malicious APK distribution channels",
                "Implement code signing verification"
            ])
        elif threat_type == "Ransomware":
            recommendations.extend([
                "Maintain regular backups outside main network",
                "Implement network segmentation",
                "Deploy ransomware-specific detection tools"
            ])
        elif threat_type == "Data Breach":
            recommendations.extend([
                "Conduct forensic investigation",
                "Reset all exposed credentials",
                "Review data access logs and permissions"
            ])
        else:
            recommendations.extend([
                f"Monitor for {threat_type.lower()} indicators",
                "Update detection signatures and rules",
                "Review access logs for suspicious activity"
            ])
        
        if attack_vector == "Email":
            recommendations.append("Review email security configurations")
        elif attack_vector == "Mobile":
            recommendations.append("Review mobile device management policies")
        elif attack_vector == "Network":
            recommendations.append("Strengthen network perimeter defenses")
        
        if ioc_count > 10:
            recommendations.append("Add extracted IOCs to threat intelligence feeds")
        
        return recommendations[:5]
    
    @staticmethod
    def calculate_confidence(threat_type, ioc_count, organizations_count, location_count):
        """Calculate dynamic confidence score"""
        score = 50
        if threat_type and threat_type != "Malware":
            score += 15
        score += min(ioc_count * 5, 20)
        score += min(organizations_count * 5, 15)
        score += min(location_count * 3, 10)
        return min(max(score, 20), 95)
    
    @staticmethod
    def analyze(text_content):
        """Main analysis pipeline - returns compatible threat analysis"""
        if not text_content or len(text_content.strip()) < 20:
            return {
                "threat_type": "Unknown",
                "category": "Other",
                "risk_score": 2,
                "confidence": 20,
                "summary": "Insufficient data for analysis",
                "recommendation": "Analyze more detailed threat information",
                "mitre_attack": [],
                "threat_actors": ["Unknown"],
                "attack_vector": "Unknown",
                "indicators_of_compromise": {
                    "domains": [],
                    "ips": [],
                    "urls": [],
                    "emails": [],
                    "telegram_handles": [],
                    "phone_numbers": [],
                    "crypto_wallets": [],
                    "hashes": []
                }
            }
        
        # Extract all data
        threat_type, threat_confidence = OfflineAnalyzer.extract_threat_type(text_content)
        organizations = OfflineAnalyzer.extract_organizations(text_content)
        locations = OfflineAnalyzer.extract_locations(text_content)
        iocs = OfflineAnalyzer.extract_iocs(text_content)
        attack_vector = OfflineAnalyzer.detect_attack_vector(text_content)
        
        ioc_count = sum(len(v) for v in iocs.values() if isinstance(v, list))
        
        # Generate dynamic content
        summary = OfflineAnalyzer.generate_summary(text_content, threat_type, organizations, ioc_count)
        recommendations = OfflineAnalyzer.generate_recommendations(threat_type, attack_vector, ioc_count)
        confidence = OfflineAnalyzer.calculate_confidence(threat_type, ioc_count, len(organizations), len(locations))
        
        # Calculate risk score
        risk_score = (threat_confidence / 100.0 * 0.5) + (confidence / 100.0 * 0.3) + (min(ioc_count, 10) / 10.0 * 0.2)
        risk_score = round(risk_score * 10, 1)
        
        mitre_techniques = OfflineAnalyzer.MITRE_MAPPING.get(threat_type, ["T1204.002"])
        
        # Return format compatible with upload routes
        return {
            "threat_type": threat_type,
            "category": "Cybercrime",
            "risk_score": risk_score,
            "confidence": confidence,
            "summary": summary,
            "recommendation": " ".join(recommendations),
            "mitre_attack": mitre_techniques,
            "threat_actors": ["Unknown Threat Actor"],
            "attack_vector": attack_vector,
            "malware_family": "",
            "indicators_of_compromise": {
                "domains": iocs.get("domains", []),
                "ips": iocs.get("ips", []),
                "urls": iocs.get("urls", []),
                "emails": iocs.get("emails", []),
                "telegram_handles": iocs.get("telegram_handles", []),
                "phone_numbers": iocs.get("phone_numbers", []),
                "crypto_wallets": iocs.get("crypto_wallets", []),
                "hashes": iocs.get("hashes", [])
            }
        }
