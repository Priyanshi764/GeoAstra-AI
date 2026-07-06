import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import './App.css';

// Import Pages
import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import Upload from './pages/Upload/Upload';
import HeatMap from './pages/HeatMap/pages/HeatMap/HeatMap';
import LiveFeed from './pages/LiveFeed/LiveFeed';
import Analytics from './pages/Analytics/Analytics';
import Investigation from './pages/Investigation/Investigation';
import Reports from './pages/Reports/Reports';
import Assistant from './pages/Assistant/Assistant';
import Settings from './pages/Settings/Settings';
import CyberZones from './pages/CyberZones/CyberZones';
import GeofenceAlerts from './pages/GeofenceAlerts/GeofenceAlerts';

// Protected Route Component
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = React.useContext(AuthContext);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        background: '#0B1220',
        color: '#2563eb',
        fontSize: '20px'
      }}>
        Loading...
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
}

function AppContent() {
  const { isAuthenticated, loading } = React.useContext(AuthContext);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        background: '#0B1220',
        color: '#2563eb',
        fontSize: '20px'
      }}>
        Loading...
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} />
      
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/upload"
        element={
          <ProtectedRoute>
            <Upload />
          </ProtectedRoute>
        }
      />
      <Route
        path="/cyber-zones"
        element={
          <ProtectedRoute>
            <CyberZones />
          </ProtectedRoute>
        }
      />
      <Route
        path="/geofence-alerts"
        element={
          <ProtectedRoute>
            <GeofenceAlerts />
          </ProtectedRoute>
        }
      />
      <Route
        path="/heatmap"
        element={
          <ProtectedRoute>
            <HeatMap />
          </ProtectedRoute>
        }
      />
      <Route
        path="/live-feed"
        element={
          <ProtectedRoute>
            <LiveFeed />
          </ProtectedRoute>
        }
      />
      <Route
        path="/analytics"
        element={
          <ProtectedRoute>
            <Analytics />
          </ProtectedRoute>
        }
      />
      <Route
        path="/investigation"
        element={
          <ProtectedRoute>
            <Investigation />
          </ProtectedRoute>
        }
      />
      <Route
        path="/reports"
        element={
          <ProtectedRoute>
            <Reports />
          </ProtectedRoute>
        }
      />
      <Route
        path="/assistant"
        element={
          <ProtectedRoute>
            <Assistant />
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <Settings />
          </ProtectedRoute>
        }
      />
      
      <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <div style={{ background: '#0B1220', minHeight: '100vh' }}>
        <Router>
          <AppContent />
        </Router>
      </div>
    </AuthProvider>
  );
}

export default App;
