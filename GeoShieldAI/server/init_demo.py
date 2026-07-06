"""
Initialize Demo Data for GeoShield AI
Creates sample users, protected assets, and threat intelligence
"""
from models.user import User
from models.protected_asset import ProtectedAsset
from models.threat import Threat
from models.alert import Alert
from datetime import datetime, timedelta
import random

def create_demo_users():
    """Create demo users"""
    demo_users = [
        {
            "email": "officer@geoastra.ai",
            "password": "password",
            "name": "Demo Officer",
            "role": "officer"
        },
        {
            "email": "admin@geoastra.ai",
            "password": "password",
            "name": "Admin User",
            "role": "admin"
        }
    ]
    
    for user_data in demo_users:
        result = User.create_user(
            email=user_data['email'],
            password=user_data['password'],
            name=user_data['name'],
            role=user_data['role']
        )
        print(f"User created: {user_data['email']} - {result}")

def create_demo_threats():
    """Create demo threat intelligence"""
    districts = ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"]
    threat_types = ["Ransomware", "Phishing", "Malware", "DDoS", "Data Breach"]
    categories = ["APT", "Cybercrime", "Hacktivism", "Insider Threat"]
    
    for i in range(10):
        threat_data = {
            "source": "demo_data",
            "threat_type": random.choice(threat_types),
            "category": random.choice(categories),
            "risk_score": random.uniform(3, 9.5),
            "confidence": random.randint(60, 100),
            "summary": f"Demo threat {i+1} - Automated security incident",
            "recommendation": "Investigate and implement security measures",
            "mitre_attack": ["T1021.001", "T1566.002"],
            "organizations": ["AIIMS Bhopal", "SBI Bhopal"],
            "districts": random.sample(districts, random.randint(1, 3)),
            "state": "Madhya Pradesh",
            "threat_actors": ["APT28", "Lazarus Group"],
            "attack_vector": "Email",
            "malware_family": "Emotet",
            "iocs": {
                "domains": ["evil.com", "malware.net"],
                "ips": ["192.168.1.1"],
                "urls": ["http://malware.com/payload"]
            },
            "created_by": "system"
        }
        
        result = Threat.create_threat(threat_data)
        print(f"Threat created: {result}")

def main():
    """Run initialization"""
    print("Starting GeoAstra AI Demo Data Initialization...")
    print("\n" + "="*50)
    print("Creating Demo Users...")
    print("="*50)
    create_demo_users()
    
    print("\n" + "="*50)
    print("Creating Demo Threats...")
    print("="*50)
    create_demo_threats()
    
    print("\n" + "="*50)
    print("Demo Data Initialization Complete!")
    print("="*50)
    print("\nDemo Credentials:")
    print("Email: officer@geoastra.ai")
    print("Password: password")

if __name__ == "__main__":
    main()
