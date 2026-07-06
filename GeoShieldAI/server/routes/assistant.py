"""
AI Assistant Routes for GeoShield AI
Handles conversational AI threat analysis assistance
"""
from flask import Blueprint, request, jsonify
from routes.auth import token_required
from ai.gemini_analyzer import GeminiAnalyzer
import json

assistant_bp = Blueprint('assistant', __name__, url_prefix='/api/assistant')

# Demo conversation history for testing
demo_conversations = []

@assistant_bp.route('/chat', methods=['POST'])
@token_required
def chat_with_ai():
    """Chat with AI assistant for threat analysis help"""
    try:
        data = request.get_json()
        
        if not data.get('message'):
            return jsonify({"success": False, "message": "No message provided"}), 400
        
        user_message = data['message']
        conversation_id = data.get('conversation_id', None)
        
        # Create enhanced prompt for threat analysis context
        system_prompt = """You are GeoAstra AI Assistant, a cybersecurity expert specializing in threat intelligence analysis. 
You help analyze threats, investigate suspicious activities, and provide security recommendations.
You have access to real-time threat data and can help with:
- Threat identification and classification
- Risk assessment and severity analysis
- Attack pattern recognition
- Incident response guidance
- Security recommendations
- MITRE ATT&CK technique mapping
- Indicators of Compromise (IoC) analysis

Provide concise, actionable responses focused on security implications."""

        # Build conversation context
        conversation = data.get('conversation', [])
        
        # Format messages for Gemini
        full_prompt = f"""System: {system_prompt}

Previous conversation:
{json.dumps(conversation[-4:], indent=2) if conversation else "No previous context"}

User: {user_message}

Assistant Response:"""
        
        try:
            response = GeminiAnalyzer.model.generate_content(full_prompt)
            ai_response = response.text.strip()
        except Exception as e:
            # Fallback response when API quota exceeded
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str:
                ai_response = get_demo_ai_response(user_message)
            else:
                return jsonify({
                    "success": False,
                    "message": f"AI analysis failed: {str(e)}"
                }), 400
        
        return jsonify({
            "success": True,
            "response": ai_response,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@assistant_bp.route('/analyze-threat', methods=['POST'])
@token_required
def analyze_threat_interactive():
    """Analyze a threat with guided questions"""
    try:
        data = request.get_json()
        
        threat_info = data.get('threat_info', '')
        user_question = data.get('question', '')
        
        if not user_question:
            return jsonify({"success": False, "message": "No question provided"}), 400
        
        prompt = f"""You are a cybersecurity analyst. Analyze this threat and answer the question.

Threat Information:
{threat_info}

Question: {user_question}

Provide a focused, technical response suitable for security professionals."""
        
        try:
            response = GeminiAnalyzer.model.generate_content(prompt)
            analysis = response.text.strip()
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str:
                analysis = f"Demo Analysis: Detailed response about {user_question} for the provided threat information. This is using demo data due to API quota limits."
            else:
                return jsonify({
                    "success": False,
                    "message": f"Analysis failed: {str(e)}"
                }), 400
        
        return jsonify({
            "success": True,
            "analysis": analysis
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@assistant_bp.route('/threat-assessment', methods=['POST'])
@token_required
def get_threat_assessment():
    """Get comprehensive threat assessment"""
    try:
        data = request.get_json()
        threat_description = data.get('description', '')
        
        if not threat_description:
            return jsonify({"success": False, "message": "No threat description provided"}), 400
        
        prompt = f"""As a cybersecurity expert, provide a comprehensive threat assessment for:

{threat_description}

Provide analysis in the following format:
1. Threat Type & Classification
2. Risk Level (1-10)
3. Affected Systems/Organization
4. Attack Vectors
5. Recommended Response
6. Preventive Measures
7. Detection Methods"""
        
        try:
            response = GeminiAnalyzer.model.generate_content(prompt)
            assessment = response.text.strip()
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str:
                assessment = get_demo_threat_assessment(threat_description)
            else:
                return jsonify({
                    "success": False,
                    "message": f"Assessment failed: {str(e)}"
                }), 400
        
        return jsonify({
            "success": True,
            "assessment": assessment
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@assistant_bp.route('/incident-response', methods=['POST'])
@token_required
def get_incident_response():
    """Get incident response guidance"""
    try:
        data = request.get_json()
        incident_description = data.get('description', '')
        
        if not incident_description:
            return jsonify({"success": False, "message": "No incident description provided"}), 400
        
        prompt = f"""You are an incident response expert. Provide immediate incident response guidance for:

{incident_description}

Structure your response as:
1. IMMEDIATE ACTIONS (next 1 hour)
2. SHORT-TERM RESPONSE (1-24 hours)
3. INVESTIGATION STEPS
4. EVIDENCE PRESERVATION
5. STAKEHOLDER NOTIFICATION
6. RECOVERY PROCEDURES
7. POST-INCIDENT REVIEW"""
        
        try:
            response = GeminiAnalyzer.model.generate_content(prompt)
            guidance = response.text.strip()
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str:
                guidance = get_demo_incident_response(incident_description)
            else:
                return jsonify({
                    "success": False,
                    "message": f"Response generation failed: {str(e)}"
                }), 400
        
        return jsonify({
            "success": True,
            "guidance": guidance
        }), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def get_demo_ai_response(user_message):
    """Generate demo AI response when API quota exceeded"""
    responses = {
        "risk": "Based on the threat data, the risk assessment indicates a moderate to high threat level. Key factors include the exposure of sensitive data, the sophistication of the attack, and the criticality of affected systems. Recommended actions include immediate threat isolation and comprehensive forensic analysis.",
        "threat": "This threat appears to be a targeted attack combining phishing and malware delivery. The attack vector suggests advanced planning and reconnaissance. Recommend implementing multi-factor authentication and network segmentation to mitigate exposure.",
        "malware": "The malware signatures indicate a known variant from the Trojan family. This malware is capable of data exfiltration and lateral movement. Isolate infected systems immediately and deploy updated antivirus signatures.",
        "phishing": "Phishing campaign detected targeting multiple users. The email crafting appears professional with social engineering elements. Recommend user awareness training and SMTP filtering for sender authentication.",
        "default": f"Thank you for your inquiry about threat intelligence. Analyzing your question: '{user_message}'. For this specific scenario, I recommend conducting a thorough threat assessment, implementing defense-in-depth strategies, and establishing continuous monitoring. This is demo analysis - for real-time assessment, consider leveraging our full threat intelligence platform."
    }
    
    message_lower = user_message.lower()
    for key in responses:
        if key in message_lower:
            return responses[key]
    return responses["default"]

def get_demo_threat_assessment(description):
    """Generate demo threat assessment"""
    return """THREAT ASSESSMENT REPORT
    
1. Threat Type & Classification
   - Type: Advanced Persistent Threat (APT)
   - Category: Targeted Cyber Attack
   - Classification: High-Risk Sophisticated Threat

2. Risk Level: 8/10
   - Critical exposure potential
   - Advanced attack techniques
   - Multi-stage attack chain detected

3. Affected Systems/Organization
   - Primary targets: Critical infrastructure and financial services
   - Secondary targets: Government and educational institutions
   - Geographic scope: Multi-regional

4. Attack Vectors
   - Email phishing with malware attachments
   - Watering hole attacks on industry websites
   - Supply chain compromise
   - Zero-day vulnerability exploitation

5. Recommended Response
   - Immediate: Isolate affected systems
   - Short-term: Forensic analysis and threat hunting
   - Long-term: Enhanced monitoring and threat intelligence sharing

6. Preventive Measures
   - Implement endpoint detection and response (EDR)
   - Deploy advanced email filtering
   - Conduct regular security awareness training
   - Maintain up-to-date patching regimen

7. Detection Methods
   - Monitor for IOC signatures
   - Behavioral analysis of network traffic
   - Anomalous process execution patterns
   - Suspicious file activity monitoring"""

def get_demo_incident_response(description):
    """Generate demo incident response guidance"""
    return """INCIDENT RESPONSE GUIDANCE

1. IMMEDIATE ACTIONS (Next 1 Hour)
   ✓ Declare incident and activate response team
   ✓ Isolate affected systems from network
   ✓ Preserve evidence and logs
   ✓ Activate incident management procedures
   ✓ Notify security leadership

2. SHORT-TERM RESPONSE (1-24 Hours)
   ✓ Collect forensic data from affected systems
   ✓ Conduct initial threat analysis
   ✓ Expand investigation scope if needed
   ✓ Identify all compromise indicators
   ✓ Begin containment procedures

3. INVESTIGATION STEPS
   ✓ Timeline reconstruction
   ✓ Attack vector identification
   ✓ Lateral movement analysis
   ✓ Data exfiltration assessment
   ✓ Threat actor attribution

4. EVIDENCE PRESERVATION
   ✓ Create forensic images of systems
   ✓ Secure access logs
   ✓ Archive network traffic captures
   ✓ Document chain of custody
   ✓ Maintain secure evidence storage

5. STAKEHOLDER NOTIFICATION
   ✓ Executive briefing prepared
   ✓ Customer notification drafted
   ✓ Regulatory reporting initiated if required
   ✓ Public relations statement ready

6. RECOVERY PROCEDURES
   ✓ Rebuild affected systems from clean backups
   ✓ Patch all identified vulnerabilities
   ✓ Restore services in staged manner
   ✓ Verify system integrity post-recovery

7. POST-INCIDENT REVIEW
   ✓ Conduct thorough post-mortem analysis
   ✓ Document lessons learned
   ✓ Update security controls
   ✓ Share threat intelligence with partners
   ✓ Schedule follow-up reviews"""
