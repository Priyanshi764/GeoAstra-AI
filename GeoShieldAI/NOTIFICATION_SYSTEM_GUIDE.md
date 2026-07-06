# GeoShield AI - Notification System Documentation

## 📱 Overview

The notification system provides real-time alerts and updates to users through an interactive notification panel in the navbar. It features automatic polling, badge counts, and actionable notifications.

---

## 🎯 Features

### 1. **Notification Bell Icon**
- Located in the top-right navbar
- Shows red badge with unread count (9+ if more than 9)
- Pulsing animation on badge for visual attention
- Click to open/close notification panel

### 2. **Notification Panel**
- Beautiful dropdown panel with glassmorphism effect
- Displays up to 10 most recent notifications
- Shows unread count badge
- Smooth animations when opening/closing
- Mobile-friendly design

### 3. **Notification Items**
Each notification displays:
- **Icon**: Type-specific emoji (🔴 critical, 🟠 high, 🟡 medium, ⚠️ incident, ℹ️ system)
- **Title**: Main notification heading
- **Message**: Detailed notification text (truncated to 2 lines)
- **Time**: Relative time (e.g., "5m ago", "1h ago")
- **Actions**: Mark as read, Delete (show on hover)
- **Color Border**: Left border indicates severity (red for critical, orange for high)

### 4. **Notification Types**
- **Threat**: Security threats detected
- **Incident**: Incident creation and updates
- **System**: System messages and updates

### 5. **Severity Levels**
- 🔴 **Critical** (risk 8+): Red badge and border
- 🟠 **High** (risk 6-7): Orange badge and border
- 🟡 **Medium** (risk 4-5): Yellow badge
- 🟢 **Low** (risk 0-3): Green badge

---

## 🔌 Backend API Endpoints

### Get Notifications
```
GET /api/user/notifications
Query Parameters:
  - limit: number (default: 20, max: 100)
  - skip: number (default: 0, for pagination)

Headers:
  Authorization: Bearer TOKEN

Response:
{
  "success": true,
  "notifications": [
    {
      "_id": "notification_id",
      "user_id": "user_id",
      "type": "threat|incident|system",
      "title": "Critical Threat Detected",
      "message": "High-risk malware detected targeting SBI...",
      "severity": "critical|high|medium|low",
      "created_at": "2026-07-04T10:30:00Z",
      "is_read": false
    }
  ],
  "unread": 3,
  "count": 10
}
```

### Mark Notification as Read
```
PUT /api/user/notifications/{notification_id}/read

Headers:
  Authorization: Bearer TOKEN

Response:
{
  "success": true,
  "message": "Notification marked as read"
}
```

### Delete Notification
```
DELETE /api/user/notifications/{notification_id}

Headers:
  Authorization: Bearer TOKEN

Response:
{
  "success": true,
  "message": "Notification deleted"
}
```

---

## 💾 Database Schema

### Notifications Collection
```json
{
  "_id": ObjectId,
  "user_id": "user_id_string",
  "type": "threat|incident|system",
  "title": "Notification Title",
  "message": "Detailed notification message",
  "severity": "critical|high|medium|low",
  "threat_id": "threat_id (if applicable)",
  "incident_id": "incident_id (if applicable)",
  "metadata": {
    "risk_score": 8.5,
    "organization": "SBI",
    "district": "Bhopal"
  },
  "created_at": ISODate,
  "updated_at": ISODate,
  "is_read": false,
  "read_at": null
}
```

---

## 🔄 How It Works

### Notification Flow

```
1. Threat Detected by AI Analysis
   ↓
2. Risk Score Calculated
   ↓
3. If High/Critical → Notification Created
   ↓
4. Saved to Database
   ↓
5. Polled by Frontend (every 30s)
   ↓
6. Displayed in Real-time
   ↓
7. User Interacts (read/delete)
```

### Auto-Polling
- Frontend polls `/api/user/notifications` every 30 seconds
- Updates notification list and unread count
- Shows animations for new notifications

### Manual Refresh
- User can click "View All Notifications" to go to Settings page
- Manual API call can be triggered from Navbar component

---

## 🔐 Frontend Components

### Navbar.jsx
**Location**: `client/src/components/navbar/Navbar.jsx`

**Key Features**:
- Manages notification state (open/closed)
- Fetches notifications on mount
- Auto-refreshes every 30 seconds
- Handles mark as read action
- Handles delete action
- Displays demo notifications if API fails

**Functions**:
```javascript
fetchNotifications()        // Get notifications from API
markAsRead(id)              // Mark notification as read
deleteNotification(id)      // Delete notification
getNotificationIcon(type)   // Get emoji based on type
formatTime(timestamp)       // Format relative time
```

### Navbar.css
**Location**: `client/src/components/navbar/Navbar.css`

**Key Styles**:
- `.notification-wrapper`: Relative positioning wrapper
- `.notification-panel`: Dropdown panel with animations
- `.notification-item`: Individual notification item
- `.notification-badge`: Red badge on bell icon with pulse animation
- `.notification-overlay`: Click-outside detection

---

## 🧠 Auth Context Integration

### AuthContext.jsx
**Location**: `client/src/context/AuthContext.jsx`

**New Features**:
- Global notification state management
- Fetches notifications on login
- Auto-polls every 30 seconds
- Provides notification actions to all components

**Context Values**:
```javascript
{
  notifications,              // Array of notification objects
  unreadCount,               // Number of unread notifications
  markNotificationAsRead(),   // Mark notification as read
  deleteNotification(),       // Delete notification
  fetchNotifications()        // Manual fetch trigger
}
```

---

## 📊 Notification Creation

### When Notifications Are Created

1. **Threat Alert** (via AI Analysis)
   ```python
   if risk_score >= ALERT_THRESHOLD:
       create_notification(
           type="threat",
           title=f"{'Critical' if risk_score >= 8 else 'High'} Threat",
           message=threat_summary,
           severity=calculate_severity(risk_score),
           threat_id=threat_id,
           metadata={...}
       )
   ```

2. **Incident Creation**
   ```python
   if risk_score >= 8:  # Auto-incident for critical
       create_notification(
           type="incident",
           title="Critical Incident Created",
           message=f"Incident ticket created for {threat_type}",
           severity="critical",
           incident_id=incident_id
       )
   ```

3. **System Events**
   ```python
   create_notification(
       type="system",
       title="System Event",
       message="System maintenance scheduled...",
       severity="low"
   )
   ```

---

## 🎨 UI/UX Design

### Notification Panel Layout
```
┌─────────────────────────────────┐
│ Notifications      [3 new]      │ ← Header
├─────────────────────────────────┤
│ 🔴 Critical Threat              │
│    Malware detected...           │
│    5 minutes ago                 │
│                            ✓  ✕  │ ← Actions on hover
├─────────────────────────────────┤
│ 🟠 Phishing Campaign            │
│    New phishing emails...        │
│    20 minutes ago                │
├─────────────────────────────────┤
│ ... more notifications ...       │
├─────────────────────────────────┤
│ View All Notifications →         │ ← Footer
└─────────────────────────────────┘
```

### Responsive Behavior
- **Desktop (1024px+)**: 380px wide panel on right side
- **Tablet (768px-1024px)**: 320px wide panel
- **Mobile (<768px)**: Full-screen modal from bottom

---

## 🎯 User Interactions

### Click Bell Icon
```
1. User clicks notification bell
2. Panel slides in with animation
3. Notifications displayed
4. Can scroll if > 5 notifications
```

### Mark As Read
```
1. Hover over notification
2. Green checkmark button appears
3. Click to mark as read
4. Notification dimmed, unread count decreased
5. API called to persist state
```

### Delete Notification
```
1. Hover over notification
2. Red X button appears
3. Click to delete
4. Notification removed from list
5. Animation out effect
```

### View All Notifications
```
1. Click "View All Notifications →"
2. Navigate to Settings page
3. Notification panel auto-closes
4. Settings page shows full notification history
```

---

## ⚙️ Configuration

### Polling Interval
**Location**: `AuthContext.jsx` line ~31
```javascript
const pollInterval = setInterval(fetchNotifications, 30000); // 30 seconds
```

### Maximum Notifications to Fetch
**Location**: `Navbar.jsx` line ~56
```javascript
const response = await axios.get(`${API_BASE_URL}/user/notifications?limit=10`);
```

### Demo Notifications (Fallback)
**Location**: `Navbar.jsx` line ~85-105
```javascript
const getDemoNotifications = () => [...]
```

---

## 🧪 Testing

### Test 1: View Notifications
1. Login to application
2. Look for red badge on bell icon
3. Click bell icon
4. Panel should slide in
5. Notifications should display

### Test 2: Mark as Read
1. Hover over unread notification
2. Green checkmark appears
3. Click checkmark
4. Notification should dim
5. Unread count should decrease

### Test 3: Delete Notification
1. Hover over notification
2. Red X button appears
3. Click X
4. Notification should disappear

### Test 4: Auto-Refresh
1. Wait 30+ seconds without interaction
2. New notification should appear if available
3. Unread count should update

### Test 5: Responsive Design
1. Test on desktop (1024px+)
2. Test on tablet (768px)
3. Test on mobile (<480px)
4. Panel should adapt to screen size

---

## 🔍 Troubleshooting

### Notifications Not Showing
```
1. Check browser console (F12)
2. Verify token is valid
3. Check API endpoint: http://127.0.0.1:5000/api/user/notifications
4. Ensure user is logged in
5. Check network tab for API calls
```

### Badge Not Updating
```
1. Check AuthContext is providing unreadCount
2. Verify fetchNotifications is being called
3. Check polling interval is working
4. Look for API errors in console
```

### Panel Not Opening
```
1. Check notification-panel CSS is loaded
2. Verify click handler is attached
3. Check z-index is not conflicting
4. Look for JavaScript errors in console
```

### Animations Not Smooth
```
1. Check browser supports CSS animations
2. Verify Framer Motion is installed
3. Check for hardware acceleration
4. Look at browser performance metrics
```

---

## 📈 Future Enhancements

1. **Sound Notifications**
   - Play sound for critical alerts
   - User-configurable alert sounds

2. **Desktop Notifications**
   - Browser push notifications
   - Even when tab is not focused

3. **Email Notifications**
   - Daily digest emails
   - Critical alert emails

4. **Notification Preferences**
   - Customize notification types
   - Set notification frequency
   - Quiet hours configuration

5. **Notification History**
   - Full searchable history
   - Filter by type/severity
   - Export notifications

6. **Real-time Updates**
   - WebSocket integration
   - Real-time threat alerts
   - Instant incident notifications

7. **Smart Grouping**
   - Group similar threats
   - Collapse duplicate alerts
   - Smart bundling

---

**Last Updated**: July 4, 2026
**Status**: Production Ready ✅
**Feature Complete**: Yes ✅
