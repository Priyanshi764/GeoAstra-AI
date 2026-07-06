import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import ProtectedRoute from '../components/ProtectedRoute';

// Pages
import Login from '../pages/Login/Login';
import Dashboard from '../pages/Dashboard/Dashboard';
import Upload from '../pages/Upload/Upload';
import HeatMap from '../pages/HeatMap/pages/HeatMap/HeatMap';
import LiveFeed from '../pages/LiveFeed/LiveFeed';
import Analytics from '../pages/Analytics/Analytics';
import Investigation from '../pages/Investigation/Investigation';
import Reports from '../pages/Reports/Reports';
import Assistant from '../pages/Assistant/Assistant';
import Settings from '../pages/Settings/Settings';

export default function AppRoutes() {
  const { isAuthenticated, loading } = React.useContext(AuthContext);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        background: '#0B1220',
        color: '#fff'
      }}>
        <div style={{
          textAlign: 'center'
        }}>
          <div style={{
            width: '50px',
            height: '50px',
            border: '4px solid rgba(255,255,255,0.1)',
            borderTop: '4px solid #2563eb',
            borderRadius: '50%',
            margin: '0 auto 20px',
            animation: 'spin 1s linear infinite'
          }}></div>
          <p>Loading...</p>
        </div>
        <style>{`
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route 
          path="/login" 
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} 
        />

        {/* Protected Routes */}
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

        {/* Default redirect */}
        <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}
