import React, { useState } from 'react';
import { motion } from 'framer-motion';
import MainLayout from '../../layouts/MainLayout';
import api from '../../services/api';
import { FiUpload, FiFileText, FiCheckCircle, FiAlertCircle, FiLoader } from 'react-icons/fi';
import './LiveFeed.css';

export default function LiveFeed() {
  const [threats, setThreats] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [activeTab, setActiveTab] = useState('threats');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  React.useEffect(() => {
    fetchLiveData();
    // Refresh every 5 seconds for live effect
    const interval = setInterval(fetchLiveData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchLiveData = async () => {
    try {
      const [threatsRes, alertsRes] = await Promise.all([
        api.get('/dashboard/recent-threats?limit=15'),
        api.get('/geofence/alerts?limit=15')
      ]);
      
      if (threatsRes.data.success) {
        setThreats(threatsRes.data.threats);
      }
      if (alertsRes.data.success) {
        setAlerts(alertsRes.data.alerts);
      }
      setError('');
    } catch (err) {
      setError('Failed to load live feed updates');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (score) => {
    if (score >= 8) return '#dc2626';
    if (score >= 6) return '#f59e0b';
    if (score >= 4) return '#2563eb';
    return '#16a34a';
  };

  const getSeverityLabel = (score) => {
    if (score >= 8) return 'CRITICAL';
    if (score >= 6) return 'HIGH';
    if (score >= 4) return 'MEDIUM';
    return 'LOW';
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="live-feed-container">
          <h1>Live Threat Feed</h1>
          <div className="loading">
            <FiLoader className="spinner" size={40} />
            <p>Loading threats...</p>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="live-feed-container">
        <motion.div
          className="live-feed-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1>🔴 Live Threat Feed</h1>
          <p>Real-time threat intelligence updates</p>
          <div className="live-indicator">
            <div className="pulse"></div>
            <span>LIVE</span>
          </div>
        </motion.div>

        {error && (
          <motion.div
            className="alert alert-error"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <FiAlertCircle size={18} />
            <span>{error}</span>
          </motion.div>
        )}

        {/* Tab switchers */}
        <div style={{ display: 'flex', gap: '12px', margin: '24px 0 16px 0', borderBottom: '1px solid rgba(75, 85, 99, 0.2)', paddingBottom: '12px' }}>
          <button
            onClick={() => setActiveTab('threats')}
            style={{
              background: activeTab === 'threats' ? 'rgba(37, 99, 235, 0.2)' : 'transparent',
              color: activeTab === 'threats' ? '#3b82f6' : '#9ca3af',
              border: activeTab === 'threats' ? '1px solid #3b82f6' : '1px solid transparent',
              borderRadius: '20px',
              padding: '6px 18px',
              fontSize: '13px',
              fontWeight: '600',
              cursor: 'pointer',
              outline: 'none',
              transition: 'all 0.2s'
            }}
          >
            🔴 Live Cyber Threats
          </button>
          <button
            onClick={() => setActiveTab('alerts')}
            style={{
              background: activeTab === 'alerts' ? 'rgba(239, 68, 68, 0.2)' : 'transparent',
              color: activeTab === 'alerts' ? '#ef4444' : '#9ca3af',
              border: activeTab === 'alerts' ? '1px solid #ef4444' : '1px solid transparent',
              borderRadius: '20px',
              padding: '6px 18px',
              fontSize: '13px',
              fontWeight: '600',
              cursor: 'pointer',
              outline: 'none',
              transition: 'all 0.2s'
            }}
          >
            🚨 Geofence Breach Alerts
          </button>
        </div>

        <div className="threats-feed">
          {activeTab === 'threats' ? (
            threats.length > 0 ? (
              threats.map((threat, idx) => (
                <motion.div
                  key={threat._id || idx}
                  className="threat-item-live"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.1 }}
                >
                  <div
                    className="threat-severity-indicator"
                    style={{ borderLeftColor: getSeverityColor(threat.risk_score) }}
                  >
                    <div className="threat-header-live">
                      <div className="threat-info">
                        <h3>{threat.threat_type}</h3>
                        <span className="category">{threat.category}</span>
                        <span className="timestamp">
                          {new Date(threat.created_at).toLocaleTimeString()}
                        </span>
                      </div>
                      <div className="threat-score">
                        <div
                          className="score-badge"
                          style={{
                            background: getSeverityColor(threat.risk_score),
                          }}
                        >
                          {threat.risk_score}
                        </div>
                        <span className="severity-label">{getSeverityLabel(threat.risk_score)}</span>
                      </div>
                    </div>

                    <p className="threat-summary">{threat.summary}</p>

                    <div className="threat-details-grid">
                      {threat.organizations && threat.organizations.length > 0 && (
                        <div className="detail-item">
                          <span className="label">Targets:</span>
                          <span className="value">{threat.organizations.join(', ')}</span>
                        </div>
                      )}
                      {threat.districts && threat.districts.length > 0 && (
                        <div className="detail-item">
                          <span className="label">Districts:</span>
                          <span className="value">{threat.districts.join(', ')}</span>
                        </div>
                      )}
                      {threat.threat_actors && threat.threat_actors.length > 0 && (
                        <div className="detail-item">
                          <span className="label">Actors:</span>
                          <span className="value">{threat.threat_actors.join(', ')}</span>
                        </div>
                      )}
                      {threat.attack_vector && (
                        <div className="detail-item">
                          <span className="label">Vector:</span>
                          <span className="value">{threat.attack_vector}</span>
                        </div>
                      )}
                    </div>

                    {threat.recommendation && (
                      <div className="recommendation">
                        <strong>Recommended Action:</strong>
                        <p>{threat.recommendation}</p>
                      </div>
                    )}
                  </div>
                </motion.div>
              ))
            ) : (
              <div className="no-threats">
                <p>No threats detected in the last updates</p>
              </div>
            )
          ) : (
            alerts.length > 0 ? (
              alerts.map((alert, idx) => (
                <motion.div
                  key={alert._id || idx}
                  className="threat-item-live"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.1 }}
                >
                  <div
                    className="threat-severity-indicator"
                    style={{ borderLeftColor: alert.severity === 'critical' ? '#ef4444' : alert.severity === 'high' ? '#f97316' : '#eab308' }}
                  >
                    <div className="threat-header-live">
                      <div className="threat-info">
                        <h3 style={{ color: alert.severity === 'critical' ? '#f87171' : alert.severity === 'high' ? '#fb923c' : '#facc15', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <FiAlertCircle /> {alert.title}
                        </h3>
                        <span className="category">{alert.zone}</span>
                        <span className="timestamp">
                          {new Date(alert.created_at).toLocaleTimeString()}
                        </span>
                      </div>
                      <div className="threat-score">
                        <div
                          className="score-badge"
                          style={{
                            background: alert.severity === 'critical' ? '#ef4444' : alert.severity === 'high' ? '#f97316' : '#eab308',
                          }}
                        >
                          {alert.risk_score}
                        </div>
                        <span className="severity-label">{alert.severity?.toUpperCase()}</span>
                      </div>
                    </div>

                    <p className="threat-summary">{alert.description}</p>

                    <div className="threat-details-grid">
                      {alert.affected_assets && alert.affected_assets.length > 0 && (
                        <div className="detail-item">
                          <span className="label">Targets:</span>
                          <span className="value">{alert.affected_assets.map(a => a.asset_name).join(', ')}</span>
                        </div>
                      )}
                      <div className="detail-item">
                        <span className="label">District Zone:</span>
                        <span className="value">{alert.district} Cyber Zone</span>
                      </div>
                      <div className="detail-item">
                        <span className="label">Confidence:</span>
                        <span className="value">{alert.confidence}%</span>
                      </div>
                      <div className="detail-item">
                        <span className="label">Status:</span>
                        <span className="value" style={{ color: alert.status === 'new' ? '#60a5fa' : '#34d399', fontWeight: 'bold' }}>
                          {alert.status?.toUpperCase()}
                        </span>
                      </div>
                    </div>

                    {alert.recommended_actions && alert.recommended_actions.length > 0 && (
                      <div className="recommendation" style={{ background: 'rgba(239, 68, 68, 0.03)', borderLeftColor: alert.severity === 'critical' ? '#ef4444' : '#f97316' }}>
                        <strong>Recommended Playbook Action:</strong>
                        <ul style={{ margin: '6px 0 0 0', paddingLeft: '16px', fontSize: '12px', color: '#d1d5db' }}>
                          {alert.recommended_actions.map((act, i) => (
                            <li key={i} style={{ marginBottom: '4px' }}>{act}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </motion.div>
              ))
            ) : (
              <div className="no-threats">
                <p>No active geofence breach alerts detected</p>
              </div>
            )
          )}
        </div>
      </div>
    </MainLayout>
  );
}

