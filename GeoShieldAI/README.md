# GeoShield AI - Cyber Threat Intelligence Platform

**AI-Powered Dark Web Geofencing & Cyber Threat Intelligence Platform**

A production-ready, enterprise-grade web application for detecting, analyzing, and visualizing cyber threats in real-time using AI-powered intelligence aggregation and geofencing.

## 🎯 Overview

GeoShield AI is designed for cybercrime agencies and security operations centers to:
- Aggregate threat intelligence from multiple sources (Dark Web, OSINT, CERT-In, etc.)
- Automatically analyze threats using Google Gemini 2.5 Flash AI
- Detect targeted organizations and affected districts
- Generate risk scores and automated alerts
- Visualize threats on interactive Madhya Pradesh maps
- Generate professional reports and forecasts

## 🏗️ Project Structure

```
GeoShieldAI/
├── client/                    # React.js Frontend (Vite)
│   └── src/
│       ├── pages/            # Page components
│       ├── components/       # Reusable components
│       ├── services/         # API integration
│       ├── context/          # React context
│       ├── routes/           # Route definitions
│       ├── layouts/          # Layout components
│       └── App.jsx           # Main app
├── server/                    # Python Flask Backend
│   ├── app.py                # Flask application
│   ├── routes/               # API routes
│   ├── models/               # Database models
│   ├── ai/                   # AI services
│   ├── services/             # Business logic
│   ├── database/             # Database config
│   ├── uploads/              # File uploads
│   └── requirements.txt      # Python dependencies
└── README.md
```

## 📋 Prerequisites

- Node.js 16+ and npm/yarn
- Python 3.8+
- MongoDB Atlas account
- Google Gemini API key
- Git

## 🚀 Quick Start

### Backend Setup

1. **Navigate to server directory:**
   ```bash
   cd server
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Configure environment variables in `.env`:**
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/geoshield
   GEMINI_API_KEY=your_gemini_api_key
   SECRET_KEY=your_secret_key
   UPLOAD_FOLDER=uploads
   DEBUG=True
   ```

6. **Start backend server:**
   ```bash
   python app.py
   ```
   Server will run at `http://127.0.0.1:5000`

### Frontend Setup

1. **Navigate to client directory:**
   ```bash
   cd client
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend will run at `http://localhost:5173`

## 🔐 Default Login Credentials

**Demo Account:**
- Email: `officer@geoshield.ai`
- Password: `password`

**Note:** Create additional accounts through the registration page.

## 📚 API Documentation

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/verify-token` - Verify JWT token
- `GET /api/auth/profile` - Get user profile

### Upload Intelligence
- `POST /api/upload/document` - Upload threat intelligence document
- `POST /api/upload/manual` - Submit manual intelligence

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/recent-threats` - Get recent threats
- `GET /api/dashboard/threat-timeline` - Get threat timeline
- `GET /api/dashboard/districts-map` - Get district threat data

### Threats
- `GET /api/threats` - List all threats
- `GET /api/threats/<id>` - Get threat details
- `GET /api/threats/district/<district>` - Get threats by district
- `GET /api/threats/high-risk` - Get high-risk threats

### Alerts
- `GET /api/alerts` - List all alerts
- `GET /api/alerts/<id>` - Get alert details
- `PUT /api/alerts/<id>/read` - Mark alert as read
- `PUT /api/alerts/<id>/acknowledge` - Acknowledge alert
- `PUT /api/alerts/<id>/status` - Update alert status

## 🤖 AI Pipeline

1. **Document Upload/Manual Entry**
   - Accept CSV, TXT, JSON, PDF, DOCX files or manual text

2. **Gemini Analysis**
   - Extract threat type, category, risk score, confidence
   - Identify threat actors and MITRE ATT&CK techniques
   - Extract indicators of compromise (IOCs)

3. **Entity Extraction**
   - Identify organization names using NER
   - Extract geographic locations

4. **Entity Mapping**
   - Match organizations to protected assets in database
   - Map locations to Madhya Pradesh districts
   - Fuzzy matching with 70%+ confidence threshold

5. **Risk Calculation**
   - Threat category score (0-10)
   - Organization criticality (0-10)
   - District sensitivity (0-10)
   - IOC count (0-10)
   - Confidence level
   - Historical incidents

6. **Alert Generation**
   - Create alerts for matched protected assets
   - Set severity based on risk score
   - Store in MongoDB for tracking

## 🛡️ Protected Assets

Default protected assets in database:
- IIITDM Jabalpur (University, High Priority)
- AIIMS Bhopal (Hospital, Critical)
- SBI Bhopal (Bank, Critical)
- Collector Office Indore (Government, Critical)
- Municipal Corporation Jabalpur (Municipal, High)

## 📊 Dashboard Features

- **Real-time Stats**: Critical alerts, high-risk threats, protected assets, districts at risk
- **Recent Threats**: Latest threat intelligence
- **Threat Distribution**: Analysis by category and district
- **Heat Map**: Visual representation of threats across MP districts
- **Live Feed**: Socket.IO powered real-time updates
- **Analytics**: Charts and graphs with Recharts
- **Investigation**: Deep threat analysis tools
- **Reports**: Generate PDF reports
- **AI Assistant**: Gemini-powered chatbot for threat queries

## 🎨 Design System

- **Dark Theme**: #0B1220 background
- **Primary Color**: #2563EB (Blue)
- **Danger**: #DC2626 (Red)
- **Warning**: #F59E0B (Amber)
- **Success**: #16A34A (Green)
- **Accent**: #2563EB
- **Typography**: System fonts (Segoe UI, Roboto, etc.)

## 🔄 Tech Stack

### Frontend
- React 19 with Vite
- Tailwind CSS 4
- React Router 7
- Framer Motion (Animations)
- Axios (HTTP Client)
- Recharts (Charts)
- React Leaflet (Maps)
- React Icons
- Socket.IO Client

### Backend
- Flask 3 with Flask-CORS
- MongoDB with PyMongo
- Google Generative AI (Gemini)
- spaCy (NLP)
- Scikit-learn (ML)
- ReportLab (PDF Generation)
- Pandas (Data Processing)
- PyPDF2 (PDF Parsing)
- python-docx (DOCX Parsing)
- JWT (Authentication)

## 🚢 Deployment

### Frontend (Vercel)
1. Build: `npm run build`
2. Connect GitHub repo to Vercel
3. Set environment variables
4. Deploy

### Backend (Render)
1. Create requirements.txt
2. Connect GitHub repo to Render
3. Set environment variables
4. Deploy as Web Service

### Database (MongoDB Atlas)
- Already configured via MONGO_URI in .env

## 📝 Environment Variables

**Backend (.env):**
```
MONGO_URI=mongodb+srv://...
GEMINI_API_KEY=sk-...
SECRET_KEY=your_secret_key_here
UPLOAD_FOLDER=uploads
DEBUG=False (production)
```

**Frontend (.env.local):**
```
VITE_API_URL=http://localhost:5000/api
```

## 🔐 Security Features

- JWT authentication with 7-day expiry
- Password hashing with SHA-256
- CORS protection
- Role-based access control (Admin, Officer)
- Protected routes
- File upload validation
- Input validation and sanitization

## 📄 License

GeoShield AI - Developed for National Hackathon

## 👥 Support

For issues or questions, contact the development team.

---

**Made with ❤️ for Cybersecurity Excellence**
