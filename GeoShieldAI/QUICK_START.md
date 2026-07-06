# GeoShield AI - Quick Start Guide

## ⚡ Get Running in 5 Minutes

### Prerequisites Check
```bash
node --version      # Should be 16+
python --version    # Should be 3.8+
```

### Step 1: Backend Setup (2 minutes)

**Windows:**
```bash
cd server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**macOS/Linux:**
```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 2: Configure Backend

Create `server/.env`:
```
MONGO_URI=mongodb+srv://username:password@cluster0.mongodb.net/geoshield
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=change_this_to_random_string
UPLOAD_FOLDER=uploads
DEBUG=True
```

### Step 3: Start Backend

```bash
python app.py
```

Expected output:
```
* Running on http://127.0.0.1:5000
```

### Step 4: Frontend Setup (2 minutes)

**In a new terminal:**
```bash
cd client
npm install
npm run dev
```

Expected output:
```
➜  Local:   http://localhost:5173/
```

### Step 5: Login

- Open http://localhost:5173
- Email: `officer@geoshield.ai`
- Password: `password`

## 🎯 First Actions

1. **Check Dashboard**
   - View statistics and recent threats
   - Navigate to Dashboard page

2. **Upload Intelligence**
   - Go to "Upload Intelligence"
   - Try uploading a sample TXT or PDF
   - Or use "Manual Entry" to paste intelligence

3. **View Analysis Results**
   - Check threat risk scores
   - See organizations and districts affected
   - View generated alerts

## 🔧 Useful Commands

### Backend
```bash
# Start fresh with demo data
python init_demo.py

# Run backend server
python app.py

# Stop server
Ctrl+C
```

### Frontend
```bash
# Development
npm run dev

# Build for production
npm run build

# Preview build
npm run preview

# Lint code
npm run lint
```

### Database
MongoDB Atlas web interface:
- Login at https://cloud.mongodb.com
- View collections in your cluster
- Browse documents

## 📊 System Architecture

```
┌─────────────────────────────────────────────────┐
│          Frontend (React + Vite)                │
│  http://localhost:5173                          │
└────────────────┬────────────────────────────────┘
                 │ HTTP/REST (Axios)
                 ↓
┌─────────────────────────────────────────────────┐
│          Backend (Flask)                        │
│  http://127.0.0.1:5000/api                      │
│  ├── Auth routes                                │
│  ├── Upload processing                          │
│  ├── Dashboard stats                            │
│  ├── Threat queries                             │
│  └── Alert management                           │
└────────────────┬────────────────────────────────┘
                 │ PyMongo
                 ↓
┌─────────────────────────────────────────────────┐
│          MongoDB Atlas                          │
│  collections:                                   │
│  ├── users                                      │
│  ├── threats                                    │
│  ├── alerts                                     │
│  └── protected_assets                           │
└─────────────────────────────────────────────────┘
```

## 🤖 AI Analysis Flow

```
Upload Document/Text
        ↓
  ┌─────────────┐
  │   Gemini    │ → Analyze threat
  │  2.5 Flash  │ → Extract IOCs
  └─────────────┘ → Score risk
        ↓
  ┌─────────────┐
  │  Entity     │ → Find organizations
  │  Mapper     │ → Map to districts
  └─────────────┘
        ↓
  ┌─────────────┐
  │ Risk Engine │ → Calculate score
  │             │ → Create alerts
  └─────────────┘
        ↓
  Store in MongoDB
        ↓
  Display on Dashboard
```

## 🔐 Demo Credentials

```
Officer Account:
  Email: officer@geoshield.ai
  Password: password
  Role: officer

Admin Account:
  Email: admin@geoshield.ai
  Password: password
  Role: admin
```

## ⚙️ Configuration Files

### `server/.env`
```
MONGO_URI=<your-mongodb-uri>
GEMINI_API_KEY=<your-gemini-key>
SECRET_KEY=<your-secret-key>
UPLOAD_FOLDER=uploads
DEBUG=True
```

### `client/.env.local`
```
VITE_API_URL=http://localhost:5000/api
```

## 🚨 Common Issues

### Backend won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F

# Try again
python app.py
```

### Frontend won't start
```bash
# Clear cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install

# Start again
npm run dev
```

### Can't connect to MongoDB
- Check connection string
- Verify username/password
- Allow network access in MongoDB Atlas
- Check if database exists

### Gemini API errors
- Verify API key is correct
- Check if API is enabled
- Ensure you have API credits

## 📚 Important Files

| File | Purpose |
|------|---------|
| `README.md` | Full documentation |
| `SETUP_GUIDE.md` | Detailed setup |
| `PROJECT_COMPLETION_SUMMARY.md` | What's included |
| `INDEX.md` | File structure |
| `.env` | Configuration |

## 🎨 Dashboard Overview

**Stats Cards**
- Critical Alerts: Number of critical level alerts
- High Risk Threats: Threats with risk score ≥ 7
- Protected Assets: Number of monitored assets
- Districts At Risk: Number of affected districts

**Recent Threats Section**
- Latest threats from database
- Shows threat type, risk score, district

**Threat Distribution**
- Top threat categories
- Top affected districts
- Organization impact

## 🔗 Key URLs

| URL | Purpose |
|-----|---------|
| http://localhost:5173 | Frontend application |
| http://127.0.0.1:5000/api | API base URL |
| http://127.0.0.1:5000/health | Health check |
| http://cloud.mongodb.com | MongoDB dashboard |
| https://makersuite.google.com | Gemini API key |

## 📋 API Quick Reference

```
# Login
POST /api/auth/login
{
  "email": "officer@geoshield.ai",
  "password": "password"
}

# Upload Intelligence
POST /api/upload/document
(multipart form data with file)

# Get Dashboard Stats
GET /api/dashboard/stats

# List Threats
GET /api/threats?limit=10&skip=0

# List Alerts
GET /api/alerts?severity=critical
```

## 🚀 Next Steps

1. ✅ **Get running locally** (you are here)
2. 📖 **Read SETUP_GUIDE.md** for detailed setup
3. 🧪 **Test all features** - upload, view, analyze
4. 🌐 **Deploy to production** - Vercel + Render
5. 👥 **Add team members** - Create user accounts
6. 🔧 **Customize** - Modify protected assets, add integrations

## ✨ Pro Tips

1. **Demo Data**: Run `python init_demo.py` for sample threats
2. **Network Error**: Check CORS in backend if API calls fail
3. **Hot Reload**: Frontend auto-reloads on file changes
4. **API Testing**: Use Postman/Insomnia for API testing
5. **Logs**: Check browser console (F12) for frontend errors
6. **Backend Logs**: Terminal output shows Flask logs

## 🆘 Need Help?

1. Check SETUP_GUIDE.md for detailed instructions
2. Review README.md for feature overview
3. Check browser console for frontend errors (F12)
4. Check terminal for backend errors
5. Verify environment variables are set
6. Ensure all services are running

## 🎉 Success!

If you see:
- ✅ Backend running on http://127.0.0.1:5000
- ✅ Frontend running on http://localhost:5173
- ✅ Can login with demo credentials
- ✅ Dashboard shows stats

**You're all set! Welcome to GeoShield AI! 🛡️**

---

**Questions?** See INDEX.md for file locations or SETUP_GUIDE.md for detailed help.
