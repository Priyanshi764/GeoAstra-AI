import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MainLayout from '../../layouts/MainLayout';
import api from '../../services/api';
import { FiAlertTriangle, FiCheckCircle, FiChevronDown, FiShield, FiInbox, FiFilter, FiSearch, FiVolume2 } from 'react-icons/fi';
import './GeofenceAlerts.css';

export default function GeofenceAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedAlert, setExpandedAlert] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    severity: '',
    status: '',
    district: ''
  });

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000); // Poll alerts every 5 seconds
    return () => clearInterval(interval);
  }, [filters]);

  const fetchAlerts = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.severity) params.append('severity', filters.severity);
      if (filters.status) params.append('status', filters.status);
      if (filters.district) params.append('district', filters.district);
      
      const response = await api.get(`/geofence/alerts?${params.toString()}`);
      if (response.data.success) {
        setAlerts(response.data.alerts);
      }
    } catch (err) {
      console.error(err);
      setError('Failed to fetch geofence alerts');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (alertId, newStatus) => {
    try {
      const response = await api.put(`/geofence/alerts/${alertId}/status`, { status: newStatus });
      if (response.data.success) {
        // Update local state immediately
        setAlerts(alerts.map(a => a._id === alertId ? { ...a, status: newStatus } : a));
      }
    } catch (err) {
      console.error(err);
      setError('Failed to update alert status');
    }
  };

  const getSeverityBadge = (level) => {
    switch (level?.toLowerCase()) {
      case 'critical': return 'critical';
      case 'high': return 'high';
      case 'medium': return 'medium';
      default: return 'low';
    }
  };

  const getStatusLabel = (status) => {
    switch (status?.toLowerCase()) {
      case 'acknowledged': return 'Acknowledged';
      case 'investigating': return 'Investigating';
      case 'resolved': return 'Resolved';
      default: return 'New';
    }
  };

  const filteredAlerts = alerts.filter(alert => {
    const term = searchTerm.toLowerCase();
    return (
      alert.title?.toLowerCase().includes(term) ||
      alert.zone?.toLowerCase().includes(term) ||
      alert.description?.toLowerCase().includes(term) ||
      alert.affected_assets?.some(asset => asset.asset_name?.toLowerCase().includes(term))
    );
  });

  if (loading && alerts.length === 0) {
    return (
      <MainLayout>
        <div className="alerts-loading">
          <div className="spinner"></div>
          <p>Scanning geofence alert log...</p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="geofence-alerts-page">
        <div className="alerts-header">
          <div>
            <h1>🚨 Geofence Alerts</h1>
            <p>Intelligence-triggered regional zone breach notifications</p>
          </div>
          <div className="status-summary">
            <span className="badge-new">New: {alerts.filter(a => a.status === 'new').length}</span>
            <span className="badge-active">Active: {alerts.filter(a => a.status !== 'resolved').length}</span>
          </div>
        </div>

        {error && <div className="error-banner">{error}</div>}

        {/* Search & Filters */}
        <div className="alerts-search-filter">
          <div className="search-bar">
            <FiSearch />
            <input
              type="text"
              placeholder="Search alerts by zone, asset name, or keywords..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="filters-group">
            <FiFilter className="filter-icon" />
            <select
              value={filters.severity}
              onChange={(e) => setFilters({ ...filters, severity: e.target.value })}
              className="filter-select"
            >
              <option value="">All Risk Levels</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>

            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              className="filter-select"
            >
              <option value="">All Statuses</option>
              <option value="new">New</option>
              <option value="acknowledged">Acknowledged</option>
              <option value="investigating">Investigating</option>
              <option value="resolved">Resolved</option>
            </select>

            <select
              value={filters.district}
              onChange={(e) => setFilters({ ...filters, district: e.target.value })}
              className="filter-select"
            >
              <option value="">All Districts</option>
              <option value="Jabalpur">Jabalpur</option>
              <option value="Bhopal">Bhopal</option>
              <option value="Indore">Indore</option>
              <option value="Gwalior">Gwalior</option>
              <option value="Ujjain">Ujjain</option>
              <option value="Sagar">Sagar</option>
            </select>
          </div>
        </div>

        {/* Alerts List */}
        <div className="alerts-list-container">
          {filteredAlerts.length > 0 ? (
            <div className="alerts-list">
              {filteredAlerts.map((alert) => {
                const isExpanded = expandedAlert === alert._id;
                const severity = getSeverityBadge(alert.severity);
                return (
                  <motion.div
                    key={alert._id}
                    className={`alert-card-geofence severity-${severity} ${alert.status === 'new' ? 'unread-alert' : ''}`}
                    layout
                  >
                    <div
                      className="alert-card-main"
                      onClick={() => setExpandedAlert(isExpanded ? null : alert._id)}
                    >
                      <div className="alert-left">
                        <div className="alert-icon-wrapper">
                          <FiAlertTriangle className={`alert-icon ${severity}`} />
                        </div>
                        <div className="alert-meta-details">
                          <h3>{alert.title}</h3>
                          <div className="meta-row">
                            <span className="meta-item">Zone: {alert.zone}</span>
                            <span className="meta-separator">•</span>
                            <span className="meta-item">Time: {new Date(alert.created_at).toLocaleTimeString()}</span>
                            {alert.affected_assets?.length > 0 && (
                              <>
                                <span className="meta-separator">•</span>
                                <span className="meta-item warning"><FiShield /> {alert.affected_assets.length} Target(s)</span>
                              </>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="alert-right">
                        <span className={`severity-badge-text ${severity}`}>{alert.severity?.toUpperCase()}</span>
                        <span className={`status-badge-text ${alert.status}`}>{getStatusLabel(alert.status)}</span>
                        <motion.div
                          animate={{ rotate: isExpanded ? 180 : 0 }}
                          transition={{ duration: 0.2 }}
                        >
                          <FiChevronDown className="chevron" />
                        </motion.div>
                      </div>
                    </div>

                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          className="alert-expanded-content"
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.25 }}
                        >
                          <div className="expanded-divider"></div>
                          
                          <div className="expanded-grid">
                            {/* Threat Summary */}
                            <div className="expanded-section">
                              <h4>Breach Assessment</h4>
                              <p className="summary-text">{alert.description}</p>
                              
                              <div className="risk-confidence-row">
                                <div className="stat-indicator">
                                  <span className="label">Risk Score:</span>
                                  <span className="val bold text-red">{alert.risk_score}/100</span>
                                </div>
                                <div className="stat-indicator">
                                  <span className="label">AI Confidence:</span>
                                  <span className="val bold">{alert.confidence}%</span>
                                </div>
                              </div>
                            </div>

                            {/* Targeted Assets */}
                            <div className="expanded-section">
                              <h4>Targeted Infrastructure Assets ({alert.affected_assets?.length || 0})</h4>
                              {alert.affected_assets?.length > 0 ? (
                                <div className="assets-sublist">
                                  {alert.affected_assets.map((asset, i) => (
                                    <div key={i} className="asset-subitem">
                                      <FiShield className={`shield-icon ${asset.criticality}`} />
                                      <div className="subitem-info">
                                        <span className="name">{asset.asset_name}</span>
                                        <span className="details">{asset.type} • Criticality: {asset.criticality?.toUpperCase()}</span>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              ) : (
                                <p className="no-sub-items">No direct registry assets breached. General district threat.</p>
                              )}
                            </div>

                            {/* Recommended Mitigation Playbook */}
                            <div className="expanded-section full-width">
                              <h4>Recommended Cyber Mitigation Playbook</h4>
                              <div className="playbook-steps">
                                {alert.recommended_actions?.map((action, i) => (
                                  <div key={i} className="playbook-step">
                                    <span className="step-num">{i + 1}</span>
                                    <span className="step-text">{action}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>

                          <div className="alert-actions-panel">
                            {alert.status === 'new' && (
                              <button
                                className="action-btn ack-btn"
                                onClick={() => handleUpdateStatus(alert._id, 'acknowledged')}
                              >
                                Acknowledge Alert
                              </button>
                            )}
                            {alert.status !== 'resolved' && (
                              <button
                                className="action-btn resolve-btn"
                                onClick={() => handleUpdateStatus(alert._id, 'resolved')}
                              >
                                Mark Incident Resolved
                              </button>
                            )}
                            {alert.status === 'resolved' && (
                              <div className="resolved-banner-text">
                                <FiCheckCircle /> Incident Resolved & Cleared
                              </div>
                            )}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                );
              })}
            </div>
          ) : (
            <div className="no-alerts-container">
              <FiInbox size={48} />
              <h3>All Quiet in the Cyber Geofence</h3>
              <p>No active or unacknowledged geofence alerts matching your filters.</p>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
}
