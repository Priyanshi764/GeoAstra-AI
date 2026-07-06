# GeoShield AI - Settings Page Documentation

## 📋 Overview

The Settings page provides comprehensive user account management, security configuration, notification preferences, and threat analysis settings. It features a clean sidebar navigation with four main configuration areas.

**Location**: `http://localhost:5174/settings`

---

## 🎯 Feature Breakdown

### 1. **PROFILE SETTINGS** 👤

#### Features:
- **Full Name**: Edit user's full name
- **Email Address**: Display user's email (read-only for security)
- **Role**: Display user's assigned role (read-only)
  - Security Officer
  - Analyst
  - Administrator
- **Organization**: Edit organization name

#### Backend Endpoints:
```
GET  /api/user/profile            - Get current profile
POST /api/user/update-profile     - Update profile information
```

#### Data Saved:
- name
- organization
- updated_at (timestamp)

#### Validation:
- Name is required
- Email cannot be changed
- Role is managed by administrators only

---

### 2. **SECURITY SETTINGS** 🔒

#### A. Password Management
**Features**:
- Change current password
- Set new password with confirmation
- Password visibility toggle (show/hide)
- Minimum 8 characters required

**Backend Endpoint**:
```
POST /api/user/change-password
```

**Validation**:
- Current password must be correct
- New passwords must match
- Minimum 8 characters
- Different from current password

#### B. Security Options
**Features**:
- **Two-Factor Authentication**: Enable/disable 2FA
- **Session Timeout**: Configure auto-logout time (5-480 minutes)
- **IP Whitelist**: Restrict access by IP addresses
  - Supports single IPs: `192.168.1.1`
  - Supports CIDR ranges: `10.0.0.0/8`
  - Comma-separated multiple entries
- **Activity Logging**: Enable/disable audit logging

**Backend Endpoint**:
```
POST /api/user/settings         - Save security settings
GET  /api/user/activity-log     - Retrieve activity logs
```

#### Saved Settings:
```json
{
  "security": {
    "twoFactorEnabled": boolean,
    "sessionTimeout": number (minutes),
    "ipRestriction": "string (comma-separated IPs)",
    "activityLogging": boolean
  }
}
```

---

### 3. **NOTIFICATION PREFERENCES** 🔔

#### Available Notifications:

1. **Email Alerts**
   - Receive email notifications for new threats
   - Can be combined with other notification options

2. **Critical Alerts Only**
   - Only send notifications for critical threats (risk 8+)
   - Disabled if Email Alerts is unchecked

3. **Daily Digest**
   - Summary email sent daily at 9:00 AM
   - Includes new threats, alerts, and statistics

4. **Weekly Report**
   - Comprehensive threat summary sent every Monday
   - Includes trends, patterns, and recommendations

5. **Incident Notifications**
   - Instant notification when security incidents are detected
   - Higher priority than regular threat alerts

#### Backend Endpoint:
```
POST /api/user/settings         - Save notification preferences
GET  /api/user/notifications    - Retrieve user notifications
PUT  /api/user/notifications/{id}/read - Mark as read
```

#### Saved Settings:
```json
{
  "notifications": {
    "emailAlerts": boolean,
    "criticalOnly": boolean,
    "dailyDigest": boolean,
    "weeklyReport": boolean,
    "incidentNotifications": boolean
  }
}
```

---

### 4. **THREAT SETTINGS** 🛡️

#### Configuration Options:

1. **Minimum Risk Score for Alerts**
   - Slider: 0-10 scale
   - Default: 5
   - Only threats above this score trigger alerts
   - Example: Set to 8 to only get critical threat alerts

2. **Auto Create Incidents**
   - Automatically create incident tickets for critical threats
   - Only for threats with risk score 8+
   - Helps streamline incident management

3. **Threat Intelligence Sources**
   - **Internal Database**: Use your internal threat data
   - **CERT-In**: Include CERT-In threat intelligence
   - **Dark Web Monitoring**: Include dark web monitoring data
   - Multiple sources can be selected

4. **Analysis Depth**
   - **Quick**: API-only analysis (fastest)
   - **Standard**: Recommended default analysis
   - **Deep**: Full investigation with historical context (slower)

#### Backend Endpoint:
```
POST /api/user/settings         - Save threat settings
```

#### Saved Settings:
```json
{
  "threats": {
    "minRiskScore": number (0-10),
    "autoIncidentCreation": boolean,
    "threatIntelSources": array ["internal", "certin", "dark_web"],
    "analysisDepth": "quick|standard|deep"
  }
}
```

---

## 🔌 Backend API Endpoints

### User Settings Routes

#### Get User Profile
```
GET /api/user/profile
Headers: Authorization: Bearer TOKEN
Response: {
  "success": true,
  "profile": {
    "id": "user_id",
    "email": "user@example.com",
    "name": "User Name",
    "role": "officer",
    "organization": "Organization",
    "created_at": "2026-07-04T...",
    "last_login": "2026-07-04T..."
  }
}
```

#### Update Profile
```
POST /api/user/update-profile
Headers: Authorization: Bearer TOKEN
Body: {
  "name": "New Name",
  "organization": "New Organization"
}
Response: {
  "success": true,
  "message": "Profile updated successfully"
}
```

#### Change Password
```
POST /api/user/change-password
Headers: Authorization: Bearer TOKEN
Body: {
  "currentPassword": "current_pass",
  "newPassword": "new_pass_123",
  "confirmPassword": "new_pass_123"
}
Response: {
  "success": true,
  "message": "Password changed successfully"
}
```

#### Get/Update Settings
```
GET /api/user/settings
POST /api/user/settings
Headers: Authorization: Bearer TOKEN
Body: {
  "notifications": {...},
  "security": {...},
  "threats": {...}
}
```

#### Get Activity Log
```
GET /api/user/activity-log?limit=50&skip=0
Headers: Authorization: Bearer TOKEN
Response: {
  "success": true,
  "activities": [...],
  "total": number,
  "count": number
}
```

#### Get Notifications
```
GET /api/user/notifications?limit=20&skip=0
Headers: Authorization: Bearer TOKEN
Response: {
  "success": true,
  "notifications": [...],
  "unread": number,
  "count": number
}
```

#### Mark Notification as Read
```
PUT /api/user/notifications/{notification_id}/read
Headers: Authorization: Bearer TOKEN
Response: {
  "success": true,
  "message": "Notification marked as read"
}
```

---

## 💾 Data Storage

### Collections in MongoDB:

1. **users** (modified)
   - name
   - organization
   - role
   - created_at
   - last_login

2. **user_settings** (new)
   ```json
   {
     "user_id": "...",
     "preferences": {
       "notifications": {...},
       "security": {...},
       "threats": {...}
     },
     "updated_at": "..."
   }
   ```

3. **user_preferences** (new)
   ```json
   {
     "user_id": "...",
     "theme": "dark",
     "language": "en",
     "timezone": "IST",
     "dateFormat": "DD/MM/YYYY"
   }
   ```

4. **activity_logs** (new)
   ```json
   {
     "user_id": "...",
     "action": "LOGIN|UPDATE|DELETE|...",
     "resource": "profile|settings|...",
     "timestamp": "...",
     "ip_address": "..."
   }
   ```

5. **notifications** (new)
   ```json
   {
     "user_id": "...",
     "title": "...",
     "message": "...",
     "type": "threat|incident|system",
     "created_at": "...",
     "is_read": boolean
   }
   ```

---

## 🎨 UI Components

### Sidebar Navigation
- Profile
- Security
- Notifications
- Threat Settings
- Logout button

### Form Elements
- Text inputs (name, organization)
- Email input (read-only)
- Select dropdowns (role, analysis depth)
- Password inputs (with show/hide toggle)
- Checkboxes (toggles)
- Range sliders (risk score)
- Checkbox groups (threat sources)

### Feedback
- Success messages (green banner)
- Error messages (red banner)
- Loading states on buttons
- Disabled states for read-only fields

### Responsive Design
- Desktop: Sidebar + Content (2 columns)
- Tablet: Collapsible tabs + Content
- Mobile: Vertical layout with compact tabs

---

## 🔐 Security Considerations

### Password Changes
- Current password verification required
- New password hashed with bcrypt
- Minimum 8 characters enforced
- Confirmation matching required

### Session Management
- Configurable timeout (5-480 minutes)
- Auto-logout on inactivity
- Optional IP-based access restrictions
- Activity logging for audit trail

### Data Protection
- All settings encrypted at rest
- HTTPS for API communication
- JWT token validation
- User context verification on all requests

---

## ✅ Validation Rules

### Profile Settings
- ✅ Name: 1-100 characters
- ✅ Organization: 0-100 characters

### Password Settings
- ✅ Current password: Must match existing
- ✅ New password: Minimum 8 characters
- ✅ Password match: Must be identical

### Security Settings
- ✅ Session timeout: 5-480 minutes
- ✅ IP addresses: Valid IPv4 or CIDR notation

### Threat Settings
- ✅ Risk score: 0-10 scale
- ✅ Intelligence sources: At least one selected
- ✅ Analysis depth: one of (quick, standard, deep)

---

## 🧪 Testing Guide

### Test Profile Update
1. Go to Settings → Profile
2. Change your name
3. Click "Save Profile"
4. Verify success message
5. Refresh page and confirm change persists

### Test Password Change
1. Go to Settings → Security
2. Enter current password
3. Enter new password (8+ chars)
4. Confirm new password
5. Click "Update Password"
6. Verify success message
7. Try logging out and back in with new password

### Test Notification Preferences
1. Go to Settings → Notifications
2. Toggle different notification options
3. Click "Save Preferences"
4. Verify changes saved
5. Check that email alerts have dependent options

### Test Threat Settings
1. Go to Settings → Threat Settings
2. Adjust minimum risk score slider
3. Toggle auto incident creation
4. Select multiple intelligence sources
5. Choose analysis depth
6. Click "Save Threat Settings"
7. Verify settings persist

---

## 🔄 User Flow

### Typical Settings Update Flow
1. User navigates to Settings page
2. User clicks on desired settings tab
3. User makes configuration changes
4. User clicks "Save [Category]" button
5. Loading state shows while saving
6. Success/error message appears
7. Settings persist across sessions
8. User can log out with logout button

---

## 📊 Default Settings

```javascript
// Notifications (defaults)
{
  emailAlerts: true,
  criticalOnly: false,
  dailyDigest: true,
  weeklyReport: true,
  incidentNotifications: true
}

// Security (defaults)
{
  twoFactorEnabled: false,
  sessionTimeout: 30,
  ipRestriction: "",
  activityLogging: true
}

// Threats (defaults)
{
  minRiskScore: 5,
  autoIncidentCreation: true,
  threatIntelSources: ["internal", "certin"],
  analysisDepth: "standard"
}
```

---

## 🚀 Future Enhancements

1. **Two-Factor Authentication**
   - SMS codes
   - Authenticator app integration
   - Backup codes

2. **Session Management**
   - View active sessions
   - Remote logout
   - Device management

3. **API Keys**
   - Generate API tokens
   - Manage integrations
   - Revoke access

4. **Backup & Recovery**
   - Data export
   - Account recovery options
   - Backup authentication methods

5. **Audit Trail**
   - View all account changes
   - Download audit logs
   - Export activity history

---

**Last Updated**: July 4, 2026
**Status**: Production Ready ✅
**Feature Complete**: Yes ✅
