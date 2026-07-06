from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["GeoAstraAI"]

users = db["users"]

threats = db["threats"]

alerts = db["alerts"]

reports = db["reports"]

protected_assets = db["protected_assets"]

geofence_alerts = db["geofence_alerts"]
investigation_cases = db["investigation_cases"]
cyber_zones = db["cyber_zones"]