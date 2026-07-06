"""
Connectors for external Threat Intelligence feeds
"""
import requests
import feedparser
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime, timedelta

class BaseConnector:
    def __init__(self, name):
        self.name = name

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch(self):
        """Fetch and return normalized intelligence items"""
        raise NotImplementedError

    def normalize(self, raw_item):
        """Convert raw item to standardized format: {'id': str, 'text': str, 'source': str, 'timestamp': datetime}"""
        raise NotImplementedError

class URLHausConnector(BaseConnector):
    def __init__(self):
        super().__init__("URLHaus")
        self.url = "https://urlhaus.abuse.ch/downloads/csv_recent/"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch(self):
        print(f"[{self.name}] Fetching recent CSV...")
        try:
            response = requests.get(self.url, timeout=15)
            response.raise_for_status()
            
            items = []
            lines = response.text.split('\n')
            # Skip comments and header, get recent 10 to avoid overloading
            data_lines = [line for line in lines if line and not line.startswith('#')]
            
            for line in data_lines[:10]:
                parts = line.split('","')
                if len(parts) >= 6:
                    raw_id = parts[0].replace('"', '')
                    url = parts[2].replace('"', '')
                    status = parts[3].replace('"', '')
                    threat = parts[4].replace('"', '')
                    tags = parts[5].replace('"', '')
                    
                    if status == "online":
                        item_id = f"urlhaus-{raw_id}"
                        text = f"Malicious URL detected: {url}. Threat: {threat}. Tags: {tags}. Status: online."
                        items.append({
                            "id": item_id,
                            "text": text,
                            "source": self.name,
                            "timestamp": datetime.utcnow()
                        })
            return items
        except Exception as e:
            print(f"[{self.name}] Error: {str(e)}")
            return []

class PhishTankConnector(BaseConnector):
    def __init__(self):
        super().__init__("PhishTank")
        # Using alternative JSON structure or scraping if direct API is restricted,
        # PhishTank's online-valid.json is a large dump. We'll use a mocked API structure or limited fetch
        # Note: PhishTank requires API key for automated access in production. 
        # For this prototype, we'll gracefully handle it if we get blocked.
        self.url = "http://data.phishtank.com/data/online-valid.json"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch(self):
        print(f"[{self.name}] Fetching valid phishing URLs...")
        try:
            # We add a user agent to avoid basic blocks
            headers = {'User-Agent': 'GeoShieldAI-Threat-Ingestion/1.0'}
            response = requests.get(self.url, headers=headers, timeout=15)
            
            # If rate limited or restricted, return empty list
            if response.status_code != 200:
                print(f"[{self.name}] Non-200 response: {response.status_code}")
                return []
                
            data = response.json()
            items = []
            # Take only the first 5 to limit AI processing
            for raw_item in data[:5]:
                item_id = f"phishtank-{raw_item.get('phish_id')}"
                url = raw_item.get('url', '')
                target = raw_item.get('target', 'Unknown target')
                text = f"Phishing attack targeting {target} detected at URL: {url}"
                
                items.append({
                    "id": item_id,
                    "text": text,
                    "source": self.name,
                    "timestamp": datetime.utcnow()
                })
            return items
        except Exception as e:
            print(f"[{self.name}] Error: {str(e)}")
            return []

class RSSConnector(BaseConnector):
    def __init__(self, name="CyberSecurityRSS", feed_url="https://feeds.feedburner.com/TheHackersNews"):
        super().__init__(name)
        self.feed_url = feed_url

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch(self):
        print(f"[{self.name}] Fetching RSS feed from {self.feed_url}...")
        try:
            feed = feedparser.parse(self.feed_url)
            items = []
            # Take top 3 recent articles
            for entry in feed.entries[:3]:
                item_id = f"rss-{entry.link}"
                title = entry.title
                summary = entry.get('summary', '')
                # Clean simple HTML from summary (very basic cleanup)
                summary = summary.replace('<p>', '').replace('</p>', '').split('<')[0]
                
                text = f"News Alert: {title}. {summary}"
                items.append({
                    "id": item_id,
                    "text": text,
                    "source": self.name,
                    "timestamp": datetime.utcnow()
                })
            return items
        except Exception as e:
            print(f"[{self.name}] Error: {str(e)}")
            return []

class NVDConnector(BaseConnector):
    def __init__(self):
        super().__init__("NVD CVE")
        self.url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch(self):
        print(f"[{self.name}] Fetching recent CVEs...")
        try:
            # Query the last 2 hours of CVEs
            now = datetime.utcnow()
            start_date = (now - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S.000")
            end_date = now.strftime("%Y-%m-%dT%H:%M:%S.000")
            
            params = {
                "pubStartDate": start_date,
                "pubEndDate": end_date,
                "resultsPerPage": 5
            }
            response = requests.get(self.url, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"[{self.name}] Non-200 response: {response.status_code}")
                return []
                
            data = response.json()
            items = []
            
            for vuln in data.get('vulnerabilities', []):
                cve = vuln.get('cve', {})
                cve_id = cve.get('id')
                
                # Get english description
                descriptions = cve.get('descriptions', [])
                desc_text = next((d.get('value') for d in descriptions if d.get('lang') == 'en'), "No description available")
                
                item_id = f"nvd-{cve_id}"
                text = f"New vulnerability {cve_id} published: {desc_text}"
                
                items.append({
                    "id": item_id,
                    "text": text,
                    "source": self.name,
                    "timestamp": datetime.utcnow()
                })
            return items
        except Exception as e:
            print(f"[{self.name}] Error: {str(e)}")
            return []

class CISAConnector(BaseConnector):
    def __init__(self):
        super().__init__("CISA KEV")
        self.url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch(self):
        print(f"[{self.name}] Fetching Known Exploited Vulnerabilities...")
        try:
            response = requests.get(self.url, timeout=15)
            if response.status_code != 200:
                return []
                
            data = response.json()
            items = []
            
            # Sort by date added descending and take top 3
            vulnerabilities = data.get('vulnerabilities', [])
            vulnerabilities.sort(key=lambda x: x.get('dateAdded', ''), reverse=True)
            
            for vuln in vulnerabilities[:3]:
                cve_id = vuln.get('cveID')
                vendor = vuln.get('vendorProject')
                product = vuln.get('product')
                desc = vuln.get('shortDescription')
                action = vuln.get('requiredAction')
                
                item_id = f"cisa-kev-{cve_id}"
                text = f"CISA KEV Alert: {vendor} {product} is actively exploited ({cve_id}). Description: {desc}. Required action: {action}"
                
                items.append({
                    "id": item_id,
                    "text": text,
                    "source": self.name,
                    "timestamp": datetime.utcnow()
                })
            return items
        except Exception as e:
            print(f"[{self.name}] Error: {str(e)}")
            return []
