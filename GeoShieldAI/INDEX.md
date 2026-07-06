# GeoShield AI - Complete File Index

## 📂 Project Root

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `SETUP_GUIDE.md` | Detailed setup and installation instructions |
| `PROJECT_COMPLETION_SUMMARY.md` | Project completion status and features |
| `INDEX.md` | This file - directory structure |
| `start.sh` | Quick start script (Linux/macOS) |
| `start.bat` | Quick start script (Windows) |
| `.gitignore` | Git ignore rules |

## 🔧 Backend Structure (`/server`)

### Root Files
```
server/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                            # Environment configuration
├── init_demo.py                    # Demo data initialization
└── uploads/                        # File upload directory
```

### Database (`/server/database`)
```
database/
└── mongodb.py                      # MongoDB connection and initialization
```

### Models (`/server/models`)
```
models/
├── user.py                         # User model (auth, profile)
├── threat.py                       # Threat intelligence model
├── alert.py                        # Alert and notification model
└── protected_asset.py              # Protected assets/infrastructure model
```

### Routes (`/server/routes`)
```
routes/
├── auth.py                         # Authentication endpoints
├── upload.py                       # Document upload and processing
├── dashboard.py                    # Dashboard statistics
├── threats.py                      # Threat CRUD operations
└── alerts.py                       # Alert management
```

### AI Services (`/server/ai`)
```
ai/
├── gemini_analyzer.py              # Google Gemini 2.5 Flash integration
├── entity_mapper.py                # Organization and location mapping
├── risk_engine.py                  # Risk scoring algorithm
├── classifier.py                   # (placeholder for ML classifier)
├── ner.py                          # (placeholder for NER)
├── summarizer.py                   # (placeholder for summarization)
├── geofence.py                     # (placeholder for geofencing)
└── forecasting.py                  # (placeholder for forecasting)
```

### Services (`/server/services)
```
services/
└── document_parser.py              # PDF, CSV, TXT, JSON, DOCX parsing
```

## 🎨 Frontend Structure (`/client`)

### Root Files
```
client/
├── package.json                    # Node dependencies
├── vite.config.js                  # Vite configuration
├── eslint.config.js                # ESLint configuration
├── index.html                      # HTML entry point
└── .gitignore                      # Git ignore rules
```

### Public Files (`/client/public`)
```
public/
├── favicon.svg                     # Site favicon
└── icons.svg                       # Icon sprite sheet
```

### Source Files (`/client/src`)

#### Root
```
src/
├── App.jsx                         # Main app component
├── App.css                         # Global styles
├── main.jsx                        # React DOM entry point
└── index.css                       # Base styles with Tailwind
```

#### Context (`/client/src/context`)
```
context/
└── AuthContext.jsx                 # Authentication state management
```

#### Routes (`/client/src/routes)
```
routes/
├── AppRoutes.jsx                   # Main route definitions
└── ProtectedRoute.jsx              # (in components/) - Route protection
```

#### Layouts (`/client/src/layouts`)
```
layouts/
├── MainLayout.jsx                  # Main layout wrapper
└── MainLayout.css                  # Layout styles
```

#### Components

##### Navbar (`/client/src/components/navbar`)
```
navbar/
├── Navbar.jsx                      # Top navigation bar
├── Navbar.css                      # Navbar styles
├── SearchBar.jsx                   # Search component (stub)
├── LiveClock.jsx                   # Live clock display (stub)
```

##### Sidebar (`/client/src/components/sidebar`)
```
sidebar/
├── Sidebar.jsx                     # Side navigation menu
└── Sidebar.css                     # Sidebar styles
```

##### Cards (`/client/src/components/cards`)
```
cards/
└── StatCard.jsx                    # Statistics card component
```

##### Map (`/client/src/components/map`)
```
map/
└── MPMap.jsx                       # Madhya Pradesh map component
```

##### Widgets (`/client/src/components/widgets`)
```
widgets/
├── AISummaryWidget.jsx             # AI summary widget
├── AlertWidget.jsx                 # Alert widget
├── LiveFeedWidget.jsx              # Live feed widget
├── NotificationPanel.jsx           # Notifications panel
└── ThreatTrendWidget.jsx           # Threat trend widget
```

##### Other Components (`/client/src/components`)
```
components/
├── ProtectedRoute.jsx              # Route protection wrapper
├── charts/                         # Chart components (for future)
├── tables/                         # Table components (for future)
└── ui/                             # UI component library (for future)
```

#### Pages (`/client/src/pages`)

##### Dashboard (`/client/src/pages/Dashboard`)
```
Dashboard/
├── Dashboard.jsx                   # Main dashboard page
└── Dashboard.css                   # Dashboard styles
```

##### Upload (`/client/src/pages/Upload`)
```
Upload/
├── Upload.jsx                      # File upload page
└── Upload.css                      # Upload styles
```

##### HeatMap (`/client/src/pages/HeatMap/pages/HeatMap`)
```
HeatMap/
├── HeatMap.jsx                     # MP district heat map
└── HeatMap.css                     # Heat map styles
```

##### Other Pages
```
pages/
├── Login/Login.jsx                 # Authentication page
├── Login/Login.css                 # Login styles
├── LiveFeed/LiveFeed.jsx           # Live feed (stub)
├── Analytics/Analytics.jsx         # Analytics (stub)
├── Investigation/Investigation.jsx # Investigation (stub)
├── Reports/Reports.jsx             # Reports (stub)
├── Assistant/Assistant.jsx         # AI Assistant (stub)
└── Settings/Settings.jsx           # Settings (stub)
```

#### Services (`/client/src/services`)
```
services/
└── api.js                          # Axios API client with interceptors
```

#### Assets (`/client/src/assets`)
```
assets/
├── hero.png                        # Hero image
├── react.svg                       # React logo
└── vite.svg                        # Vite logo
```

#### Utils (`/client/src/utils`)
```
utils/
└── (empty - ready for utility functions)
```

#### Hooks (`/client/src/hooks`)
```
hooks/
└── (empty - ready for custom hooks)
```

## 📊 Database Collections

### users
- Stores user accounts and authentication
- Fields: _id, email, name, password_hash, role, created_at, is_active

### threats
- Stores threat intelligence
- Fields: _id, source, threat_type, category, risk_score, confidence, organizations, districts, iocs, created_at

### alerts
- Stores security alerts
- Fields: _id, threat_id, title, severity, organization, district, status, is_read, created_at

### protected_assets
- Stores critical infrastructure registry
- Fields: _id, name, type, district, criticality, coordinates, contact_info, created_at

### uploads (for future)
- Stores upload history and metadata

### reports (for future)
- Stores generated reports

### logs (for future)
- Stores audit logs

## 🔗 API Endpoint Mapping

```
/api/auth/
  ├── POST /register
  ├── POST /login
  ├── GET /verify-token
  └── GET /profile

/api/upload/
  ├── POST /document
  └── POST /manual

/api/dashboard/
  ├── GET /stats
  ├── GET /recent-threats
  ├── GET /threat-timeline
  └── GET /districts-map

/api/threats/
  ├── GET / (list)
  ├── GET /<id>
  ├── GET /district/<district>
  ├── GET /organization/<org>
  ├── GET /high-risk
  └── PUT /<id>/update

/api/alerts/
  ├── GET / (list)
  ├── GET /<id>
  ├── GET /severity/<severity>
  ├── GET /unread
  ├── PUT /<id>/read
  ├── PUT /<id>/acknowledge
  ├── PUT /<id>/status
  └── GET /summary
```

## 🔐 Environment Configuration

### Backend (.env)
```
MONGO_URI=<MongoDB connection string>
GEMINI_API_KEY=<Google Gemini API key>
SECRET_KEY=<JWT secret key>
UPLOAD_FOLDER=uploads
DEBUG=True/False
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:5000/api
```

## 📦 Dependencies

### Backend (Python)
- Flask 3.0.0
- Flask-CORS 4.0.0
- python-socketio 5.10.0
- pymongo 4.6.0
- google-generativeai 0.3.0
- python-dotenv 1.0.0
- spacy 3.7.2
- sentence-transformers 2.2.2
- scikit-learn 1.3.2
- reportlab 4.0.7
- pandas 2.1.3
- PyPDF2 3.0.1
- python-docx 0.8.11
- PyJWT 2.8.1
- werkzeug 3.0.1

### Frontend (Node)
- react 19.2.7
- react-dom 19.2.7
- react-router-dom 7.18.1
- axios 1.18.1
- framer-motion 12.42.2
- recharts 3.9.2
- react-leaflet 5.0.0
- leaflet 1.9.4
- react-icons 5.7.0
- socket.io-client 4.8.3
- tailwindcss 4.3.2

## 🚀 Startup Scripts

| File | Platform | Purpose |
|------|----------|---------|
| `start.sh` | Linux/macOS | Starts backend + frontend |
| `start.bat` | Windows | Starts backend + frontend |

## 📝 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview and features |
| `SETUP_GUIDE.md` | Installation and setup |
| `PROJECT_COMPLETION_SUMMARY.md` | Completion status |
| `INDEX.md` | This file |

## 🎯 Key Directories

```
GeoShieldAI/
├── server/                 # Backend (Python/Flask)
│   ├── app.py             # Main application
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   ├── ai/                # AI services
│   ├── services/          # Business logic
│   ├── database/          # DB config
│   └── uploads/           # File uploads
├── client/                 # Frontend (React/Vite)
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── components/    # Reusable components
│   │   ├── services/      # API client
│   │   ├── context/       # State management
│   │   ├── routes/        # Route config
│   │   └── layouts/       # Layout templates
│   └── public/            # Static files
└── docs/                   # Documentation

## 🔄 Data Flow

```
User Input (UI)
    ↓
React Component
    ↓
Axios API Call
    ↓
Flask Route Handler
    ↓
AI Service (Gemini)
    ↓
Entity Mapper
    ↓
Risk Engine
    ↓
Database (MongoDB)
    ↓
Dashboard Display
```

## ✅ Quick Reference

**Backend Start**: `cd server && python app.py`
**Frontend Start**: `cd client && npm run dev`
**Demo Login**: officer@geoshield.ai / password
**API Base**: http://127.0.0.1:5000/api
**Frontend URL**: http://localhost:5173

---

**For more details, see README.md or SETUP_GUIDE.md**

**🛡️ GeoShield AI - Complete File Index**
