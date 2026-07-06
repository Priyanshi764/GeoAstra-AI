# GeoShield AI - Testing Guide

## ✅ System Status Check

### Running Services:
- **Backend API**: `http://127.0.0.1:5000` ✅
- **Frontend UI**: `http://localhost:5174` ✅
- **Database**: MongoDB Atlas ✅

---

## 🧪 Feature Testing Guide

### 1. ANALYTICS PAGE TEST

**URL**: `http://localhost:5174/analytics`

**Steps**:
1. Login with your credentials
2. Navigate to Analytics
3. Verify you see:
   - ✅ Dashboard header with gradient
   - ✅ Time range selector buttons (7d, 30d, 90d)
   - ✅ Four metric cards (Total Alerts, Critical Alerts, Total Threats, Protected Assets)
   - ✅ Threat Types Distribution chart
   - ✅ Alert Severity Breakdown visualization
   - ✅ Top Organizations Under Threat list
   - ✅ Geographic Threat Distribution cards
   - ✅ Threat Categories table

**Expected Results**:
- All data populated from database
- Smooth animations on hover
- Responsive layout on resize
- No console errors

**Test Data Sources**:
- Data comes from `/api/dashboard/stats`
- Sample threats in database: ~10 pre-loaded threats

---

### 2. INVESTIGATION PAGE TEST

**URL**: `http://localhost:5174/investigation`

**Steps**:
1. Login and navigate to Investigation
2. Verify you see:
   - ✅ Search box
   - ✅ Three filter dropdowns (Category, Risk Level, District)
   - ✅ List of detected threats

3. Test search functionality:
   - Type "phishing" → should filter threats
   - Type "SBI" → should show organization-related threats
   - Type organization name → should find matching threats

4. Test filters:
   - **Category Filter**: Select "Malware" → shows only malware threats
   - **Risk Level Filter**: Select "High & Above" → filters by risk score
   - **District Filter**: Select "Bhopal" → shows Bhopal region threats

5. Expand a threat card:
   - Click any threat item
   - ✅ Expands to show full details
   - ✅ View: category, confidence, organization, districts, threat actors
   - ✅ Shows MITRE ATT&CK techniques
   - ✅ Displays IoCs (domains, IPs, URLs, emails, hashes)
   - ✅ See download button

6. Download a report:
   - Click "Download Report" button
   - Should save `threat_report_[ID].txt` to downloads
   - Verify file contains all threat information

**Expected Results**:
- Search instantly filters results
- Filters combine (AND logic)
- Threat expansion smooth animation
- Report download works
- No console errors

**Test Data Sources**:
- Data from `/api/threats` endpoint
- Sample threats: ~10 pre-loaded in database

---

### 3. AI ASSISTANT PAGE TEST

**URL**: `http://localhost:5174/assistant`

#### A. CHAT MODE TEST
**Steps**:
1. Click "Chat" tab (should be active by default)
2. Verify initial AI greeting message appears
3. Type a question in input box:
   - "What should I do about a phishing threat?"
   - Press Enter or click Send button

4. Verify:
   - ✅ Your message appears on right side (blue-ish)
   - ✅ AI avatar shows on left
   - ✅ AI response appears after a moment
   - ✅ Typing animation shows while AI is "thinking"
   - ✅ Multiple exchanges work (conversation history maintained)

5. Test clear button:
   - Click refresh icon button
   - Chat history clears
   - New greeting message appears

**Expected Results**:
- Smooth message flow
- Proper styling for user/AI messages
- AI responses relevant to questions
- No errors in console
- Graceful fallback with demo responses (API quota active)

#### B. THREAT ASSESSMENT TAB TEST
**Steps**:
1. Click "Threat Assessment" tab
2. Paste threat description in textarea:
```
We detected unauthorized access attempts to our banking database. 
Multiple failed login attempts from suspicious IPs in Eastern Europe. 
Systems shows signs of SQL injection attempts targeting customer records.
```

3. Click "Analyze Threat" button
4. Verify:
   - ✅ Loading state shows briefly
   - ✅ Assessment appears on right side
   - ✅ Contains threat classification, risk level, attack vectors, recommendations
   - ✅ Report is readable and formatted

5. Download report:
   - Click "Download" button
   - Saves `threat_assessment.txt`
   - Contains full analysis

**Expected Results**:
- Analysis generates successfully
- Report downloads with proper format
- Multiple assessments can be generated
- Graceful demo mode responses

#### C. INCIDENT RESPONSE TAB TEST
**Steps**:
1. Click "Incident Response" tab
2. Paste incident description:
```
We discovered that our production web server was compromised this morning.
Logs show suspicious user creation at 3:00 AM.
Data extraction detected - approximately 10GB transferred to external IP.
All web services taken offline for investigation.
```

3. Click "Generate Response Plan" button
4. Verify:
   - ✅ Generates comprehensive response plan
   - ✅ Shows immediate actions, short-term response, investigation steps
   - ✅ Includes evidence preservation guidance
   - ✅ Stakeholder notification instructions
   - ✅ Recovery procedures
   - ✅ Post-incident review steps

5. Download plan:
   - Click "Download" button
   - Saves `incident_response_plan.txt`
   - Contains structured response guidance

**Expected Results**:
- Response plan is comprehensive and actionable
- Plan downloads successfully
- Multiple incidents can be analyzed
- Structured format is easy to follow

---

## 🔧 API ENDPOINT TESTING

### Using curl or Postman:

**1. Test Analytics Endpoint**:
```bash
curl -X GET http://127.0.0.1:5000/api/dashboard/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**2. Test Threats Endpoint**:
```bash
curl -X GET "http://127.0.0.1:5000/api/threats?limit=10&min_risk=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**3. Test Assistant Chat**:
```bash
curl -X POST http://127.0.0.1:5000/api/assistant/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "What is a phishing attack?"}'
```

**4. Test Threat Assessment**:
```bash
curl -X POST http://127.0.0.1:5000/api/assistant/threat-assessment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"description": "Malware detected on server"}'
```

---

## 📊 Test Scenarios

### Scenario 1: New User Flow
1. Login to application
2. View Dashboard (default page)
3. Navigate to Analytics
4. Review threat statistics
5. Go to Investigation
6. Search for high-risk threats
7. View threat details
8. Download threat report

**Expected Time**: ~2 minutes
**Expected Result**: All pages load, data displays correctly

### Scenario 2: Security Analyst Flow
1. Login
2. Go to Investigation
3. Filter threats by category "Malware"
4. Filter by risk level "Critical"
5. Select a threat
6. Review all IoCs
7. Download investigation report
8. Go to Assistant
9. Ask AI about threat mitigation

**Expected Time**: ~3 minutes
**Expected Result**: All features work seamlessly

### Scenario 3: Incident Response Flow
1. Login
2. Go to Assistant
3. Describe incident in Incident Response tab
4. Get response plan
5. Download response plan
6. Go to Investigation
7. Search related threats
8. Build incident timeline

**Expected Time**: ~4 minutes
**Expected Result**: Cohesive incident response workflow

---

## 🐛 Debugging Tips

### If Pages Don't Load:
```bash
# Check frontend is running
netstat -ano | findstr "5174"

# Check backend is running
netstat -ano | findstr "5000"

# Check browser console (F12)
# Should show no red errors
```

### If Data is Empty:
```bash
# Verify sample threats are in database
# MongoDB:
# db.threats.countDocuments()
# Should return: 10 (or more)

# Check API response:
curl http://127.0.0.1:5000/api/dashboard/stats -H "Authorization: Bearer TOKEN"
```

### If AI Features Don't Work:
- Check `.env` file for `GEMINI_API_KEY`
- API quota may be exceeded (demo mode will activate)
- Check browser console for specific error messages

---

## ✅ Success Checklist

- [ ] Analytics page loads and displays data
- [ ] Investigation page search works
- [ ] Investigation page filters work
- [ ] Threat details expand correctly
- [ ] Reports download successfully
- [ ] AI Chat responds to messages
- [ ] Threat Assessment generates analysis
- [ ] Incident Response generates plan
- [ ] No console errors
- [ ] Responsive on mobile (test with devtools)
- [ ] All navigation links work
- [ ] Login/logout functions properly

---

## 📞 Support

If you encounter issues:

1. **Check the browser console** (F12 → Console tab)
2. **Check the backend logs** in terminal where Flask is running
3. **Verify all services are running**:
   - Backend on port 5000
   - Frontend on port 5174
   - MongoDB Atlas connection active

---

**Last Updated**: July 4, 2026
**Test Environment**: Development
**Status**: Ready for Testing ✅
