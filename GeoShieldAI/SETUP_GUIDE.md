# GeoShield AI - Complete Setup Guide

## System Requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **Node.js**: 16.0.0 or higher
- **Python**: 3.8.0 or higher
- **Git**: Latest version
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 2GB minimum

## Prerequisites Installation

### 1. Install Node.js
**Windows/macOS:**
- Download from https://nodejs.org/ (LTS version)
- Follow the installer instructions
- Verify installation: `node --version` and `npm --version`

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2. Install Python
**Windows:**
- Download from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Verify: `python --version`

**macOS:**
```bash
brew install python@3.10
```

**Linux:**
```bash
sudo apt-get install python3 python3-pip python3-venv
```

### 3. Install MongoDB Atlas

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a new project and cluster
4. Get your connection string
5. Create a database user with admin privileges
6. Allow access from your IP address (or 0.0.0.0/0 for development)

### 4. Get Google Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Enable the Generative Language API
4. Copy your API key

## Backend Setup (Complete)

### Step 1: Navigate to Server Directory
```bash
cd server
```

### Step 2: Create Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### Step 5: Create Environment File
Create `.env` file in `server/` directory:

```env
# MongoDB Configuration
MONGO_URI=mongodb+srv://username:password@cluster0.mongodb.net/geoshield?retryWrites=true&w=majority

# Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Flask Configuration
SECRET_KEY=your_super_secret_key_change_this_in_production
UPLOAD_FOLDER=uploads
DEBUG=True

# Flask Host/Port
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

**Important:** Replace the values with your actual credentials.

### Step 6: Create Upload Folder
```bash
mkdir uploads
```

### Step 7: Initialize Demo Data (Optional)
```bash
python init_demo.py
```

This creates:
- Demo user: officer@geoshield.ai / password
- Demo admin: admin@geoshield.ai / password
- Sample threats and alerts

### Step 8: Start Backend Server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Troubleshooting Backend Issues

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

**MongoDB connection error:**
- Verify connection string in `.env`
- Check if cluster is accessible from your IP
- Ensure database user has correct password

**Gemini API errors:**
- Verify API key is correct
- Check if API is enabled
- Ensure you have credits

## Frontend Setup (Complete)

### Step 1: Navigate to Client Directory
```bash
cd client
```

### Step 2: Install Node Dependencies
```bash
npm install
```

### Step 3: Create Environment File
Create `.env.local` in `client/` directory:

```env
VITE_API_URL=http://localhost:5000/api
```

### Step 4: Start Development Server
```bash
npm run dev
```

You should see:
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
```

### Troubleshooting Frontend Issues

**Port 5173 already in use:**
```bash
# The dev server will automatically use next available port
```

**Dependencies issues:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Initial System Setup

### 1. Access the Application
- Frontend: http://localhost:5173
- Backend: http://localhost:5000/api

### 2. Login with Demo Account
- **Email**: officer@geoshield.ai
- **Password**: password

### 3. Create Protected Assets (If Not Already Created)
The system initializes default protected assets on first run:
- IIITDM Jabalpur
- AIIMS Bhopal
- SBI Bhopal
- Collector Office Indore
- Municipal Corporation Jabalpur

### 4. Upload Sample Intelligence
1. Go to "Upload Intelligence"
2. Try uploading a sample CSV or TXT file with threat information
3. Or use "Manual Entry" to paste intelligence

## Production Deployment

### Backend Deployment (Render.com)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://render.com
   - Create new Web Service
   - Connect your GitHub repository
   - Set build command: `pip install -r server/requirements.txt`
   - Set start command: `cd server && python app.py`
   - Add environment variables from `.env`

3. **Production Environment Variables**
   ```
   DEBUG=False
   SECRET_KEY=generate_strong_random_key
   MONGO_URI=your_production_mongo_uri
   GEMINI_API_KEY=your_gemini_api_key
   ```

### Frontend Deployment (Vercel.com)

1. **Deploy to Vercel**
   - Go to https://vercel.com
   - Import your GitHub repository
   - Set framework to "Vite"
   - Set build command: `npm run build`
   - Set environment variables:
     ```
     VITE_API_URL=https://your-backend-url.com/api
     ```
   - Deploy

### Database Optimization

1. **Create Indexes** for MongoDB:
   ```javascript
   db.threats.createIndex({ "created_at": -1 })
   db.threats.createIndex({ "districts": 1 })
   db.threats.createIndex({ "risk_score": -1 })
   db.alerts.createIndex({ "severity": 1 })
   db.protected_assets.createIndex({ "district": 1 })
   ```

## Development Commands

### Backend

```bash
# Start development server
python app.py

# Run tests (if implemented)
pytest

# Format code
black server/

# Lint code
flake8 server/
```

### Frontend

```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code
npx prettier --write .
```

## Database Collections Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "string",
  "name": "string",
  "password_hash": "string",
  "role": "admin|officer",
  "created_at": "datetime",
  "is_active": true
}
```

### Threats Collection
```json
{
  "_id": "ObjectId",
  "source": "string",
  "threat_type": "string",
  "category": "string",
  "risk_score": 7.5,
  "confidence": 85,
  "summary": "string",
  "organizations": ["string"],
  "districts": ["string"],
  "iocs": {
    "domains": ["string"],
    "ips": ["string"]
  },
  "created_at": "datetime"
}
```

### Alerts Collection
```json
{
  "_id": "ObjectId",
  "threat_id": "string",
  "title": "string",
  "severity": "critical|high|medium|low",
  "organization": "string",
  "district": "string",
  "status": "new|acknowledged|investigating|resolved",
  "is_read": false,
  "created_at": "datetime"
}
```

## Monitoring & Logging

### Backend Logs
Logs are output to console. For production, configure logging to a file:

```python
# In app.py
import logging
logging.basicConfig(filename='geoshield.log', level=logging.INFO)
```

### Frontend Errors
Check browser console (F12 → Console tab) for errors.

## Performance Optimization

### Frontend
- Enable code splitting
- Lazy load components
- Optimize images
- Use production build: `npm run build`

### Backend
- Enable database connection pooling
- Cache frequent queries
- Use pagination for large datasets
- Monitor API response times

## Security Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS in production
- [ ] Configure CORS properly
- [ ] Validate all inputs
- [ ] Use environment variables for secrets
- [ ] Enable MongoDB authentication
- [ ] Restrict file uploads
- [ ] Implement rate limiting
- [ ] Regular security updates

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check Python version: `python --version` (should be 3.8+)
- Check if port 5000 is available
- Verify all dependencies installed: `pip list`

**Frontend won't start:**
- Check Node version: `node --version` (should be 16+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check if port 5173 is available

**Cannot connect to database:**
- Verify MongoDB connection string
- Check network access rules in MongoDB Atlas
- Ensure database user has correct permissions

**Gemini API errors:**
- Verify API key is valid and not expired
- Check API quotas and usage
- Ensure API is enabled in Google Cloud

## Support & Resources

- **MongoDB Docs**: https://docs.mongodb.com/
- **Flask Docs**: https://flask.palletsprojects.com/
- **React Docs**: https://react.dev/
- **Vite Docs**: https://vitejs.dev/
- **Gemini API**: https://ai.google.dev/

## Next Steps

1. Customize protected assets for your organization
2. Configure threat sources and integrations
3. Set up automated intelligence feeds
4. Train team on platform usage
5. Configure alerts and notifications
6. Deploy to production environment

---

**For issues or questions, please refer to the README.md or create an issue on GitHub.**

**Happy Threat Intelligence Analysis! 🛡️**
