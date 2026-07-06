import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_threat(text):

    prompt = f"""
You are an expert Cyber Threat Intelligence analyst.

Analyze the following cyber threat intelligence.

Return ONLY valid JSON.

Required JSON format:

{{
"threat_type":"",
"category":"",
"target_organization":"",
"district":"",
"state":"",
"risk":"",
"confidence":"",
"summary":"",
"recommended_action":"",
"mitre_attack":""
}}

Threat Intelligence:

{text}
"""

    response = model.generate_content(prompt)

    output = response.text.strip()

    if output.startswith("```json"):
        output = output.replace("```json","").replace("```","")

    elif output.startswith("```"):
        output = output.replace("```","")

    return json.loads(output)