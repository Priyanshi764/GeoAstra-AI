import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import MainLayout from '../../layouts/MainLayout';
import api from '../../services/api';
import { FiAlertCircle, FiTrendingUp, FiShield, FiMapPin, FiActivity, FiAlertTriangle } from 'react-icons/fi';
import '../Dashboard/Dashboard.css';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [recentThreats, setRecentThreats] = useState([]);
  const [geofenceStats, setGeofenceStats] = useState(null);
  const [recentGeofenceAlerts, setRecentGeofenceAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Segmented Tab States for uncluttered layout
  const [feedTab, setFeedTab] = useState('alerts');
  const [distTab, setDistTab] = useState('category');

  useEffect(() => {
    fetchDashboardData();
    // Poll every 5 seconds to update stats in real-time
    const interval = setInterval(fetchDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, threatsRes, geofenceStatsRes, geofenceAlertsRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/dashboard/recent-threats?limit=5'),
        api.get('/geofence/dashboard'),
        api.get('/geofence/alerts?limit=5')
      ]);

      if (statsRes.data.success) {
        setStats(statsRes.data.stats);
      }
      if (threatsRes.data.success) {
        setRecentThreats(threatsRes.data.threats);
      }
      if (geofenceStatsRes.data.success) {
        setGeofenceStats(geofenceStatsRes.data.stats);
      }
      if (geofenceAlertsRes.data.success) {
        setRecentGeofenceAlerts(geofenceAlertsRes.data.alerts);
      }
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="dashboard-loading">
          <div className="spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="dashboard">
        <motion.div
          className="dashboard-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1>Threat Intelligence Dashboard</h1>
          <p>Real-time cybersecurity threat monitoring and analysis</p>
        </motion.div>

        {error && <div className="error-banner">{error}</div>}

        {/* Stats Grid */}
        {stats && (
          <motion.div
            className="stats-grid"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ staggerChildren: 0.1 }}
          >
            <StatCard
              icon={<FiAlertCircle />}
              title="Critical Alerts"
              value={stats.alerts?.critical || 0}
              color="danger"
            />
            <StatCard
              icon={<FiTrendingUp />}
              title="High Risk Threats"
              value={stats.threats?.high_risk || 0}
              color="warning"
            />
            <StatCard
              icon={<FiShield />}
              title="Protected Assets"
              value={stats.assets?.total || 0}
              color="info"
            />
            <StatCard
              icon={<FiMapPin />}
              title="Districts At Risk"
              value={stats.coverage?.districts_with_threats || 0}
              color="success"
            />
          </motion.div>
        )}

        {/* Main Content */}
        <div className="dashboard-content">
          {/* Main Feed Column */}
          <div className="dashboard-main-column">
            <motion.div
              className="card feed-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <div className="feed-card-header">
                <div className="feed-title-section">
                  <span className="pulse-dot"></span>
                  <h2>Security Operations Center</h2>
                </div>
                <div className="feed-tabs">
                  <button 
                    className={`feed-tab-btn ${feedTab === 'alerts' ? 'active' : ''}`}
                    onClick={() => setFeedTab('alerts')}
                  >
                    Geofence Triggers ({recentGeofenceAlerts.length})
                  </button>
                  <button 
                    className={`feed-tab-btn ${feedTab === 'threats' ? 'active' : ''}`}
                    onClick={() => setFeedTab('threats')}
                  >
                    Intelligence Logs ({recentThreats.length})
                  </button>
                </div>
              </div>

              <div className="feed-content-area">
                {feedTab === 'alerts' ? (
                  <div className="alerts-list compact">
                    {recentGeofenceAlerts.length > 0 ? (
                      recentGeofenceAlerts.map((alert, idx) => (
                        <div 
                          key={alert._id || idx} 
                          className={`threat-item-compact severity-border-${alert.severity}`}
                        >
                          <div className="threat-info-main">
                            <FiAlertTriangle className="threat-list-icon alert" />
                            <span className="threat-type-name" title={alert.title}>{alert.title}</span>
                            <span className="badge mini-badge badge-zone">Zone: {alert.zone}</span>
                          </div>
                          <div className="threat-info-meta">
                            {alert.affected_assets?.length > 0 && (
                              <span className="asset-count-badge" title={alert.affected_assets.map(a => a.asset_name).join(', ')}>
                                Targets: {alert.affected_assets.length}
                              </span>
                            )}
                            <span className={`severity-pill ${alert.severity === 'critical' ? 'danger' : alert.severity === 'high' ? 'warning' : 'info'}`}>
                              Risk: {alert.risk_score.toFixed(1)}
                            </span>
                          </div>
                        </div>
                      ))
                    ) : (
                      <p className="no-data">No active geofence triggers detected.</p>
                    )}
                  </div>
                ) : (
                  <div className="threats-list compact">
                    {recentThreats.length > 0 ? (
                      recentThreats.map((threat, index) => (
                        <ThreatItem key={threat._id || index} threat={threat} />
                      ))
                    ) : (
                      <p className="no-data">No threats found</p>
                    )}
                  </div>
                )}
              </div>
            </motion.div>
          </div>

          {/* Side Distribution Column */}
          <div className="dashboard-side-column">
            {stats?.coverage && (
              <motion.div
                className="card distribution-card"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <div className="dist-card-header">
                  <h2>Threat Distribution</h2>
                  <div className="dist-tabs">
                    <button
                      className={`dist-tab-btn ${distTab === 'category' ? 'active' : ''}`}
                      onClick={() => setDistTab('category')}
                    >
                      Categories
                    </button>
                    <button
                      className={`dist-tab-btn ${distTab === 'district' ? 'active' : ''}`}
                      onClick={() => setDistTab('district')}
                    >
                      Districts
                    </button>
                  </div>
                </div>

                <div className="dist-content-area">
                  {distTab === 'category' ? (
                    <div className="category-list">
                      {stats.coverage.threat_categories?.slice(0, 5).map((cat, idx) => (
                        <div key={idx} className="category-item">
                          <span>{cat._id}</span>
                          <span className="count-badge">{cat.count} threats</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="district-list">
                      {stats.coverage.top_districts?.slice(0, 5).map((dist, idx) => (
                        <div key={idx} className="district-item">
                          <span>{dist._id}</span>
                          <span className="count-badge count-secondary">{dist.count} threats</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

function StatCard({ icon, title, value, color }) {
  return (
    <motion.div
      className={`stat-card stat-${color}`}
      whileHover={{ y: -5 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="stat-icon">{icon}</div>
      <div className="stat-content">
        <p className="stat-title">{title}</p>
        <p className="stat-value">{value}</p>
      </div>
    </motion.div>
  );
}

function ThreatItem({ threat }) {
  const getSeverityColor = (score) => {
    if (score >= 8) return 'danger';
    if (score >= 6) return 'warning';
    if (score >= 4) return 'info';
    return 'success';
  };

  return (
    <div className={`threat-item-compact severity-border-${getSeverityColor(threat.risk_score)}`}>
      <div className="threat-info-main">
        <FiShield className="threat-list-icon" />
        <span className="threat-type-name">{threat.threat_type}</span>
        <span className="badge mini-badge">{threat.category}</span>
      </div>
      <div className="threat-info-meta">
        {threat.districts?.length > 0 && (
          <span className="district-badge">{threat.districts[0]}</span>
        )}
        <span className={`severity-pill ${getSeverityColor(threat.risk_score)}`}>
          Risk: {threat.risk_score.toFixed(1)}
        </span>
      </div>
    </div>
  );
}
