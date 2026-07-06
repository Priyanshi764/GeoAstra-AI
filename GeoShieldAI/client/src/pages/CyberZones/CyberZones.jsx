import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MainLayout from '../../layouts/MainLayout';
import api from '../../services/api';
import { FiShield, FiAlertTriangle, FiActivity, FiMapPin, FiCpu, FiUser } from 'react-icons/fi';
import './CyberZones.css';

export default function CyberZones() {
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedZone, setSelectedZone] = useState(null);

  useEffect(() => {
    fetchZones();
    const interval = setInterval(fetchZones, 10000); // refresh every 10s
    return () => clearInterval(interval);
  }, []);

  const fetchZones = async () => {
    try {
      const response = await api.get('/geofence/zones');
      if (response.data.success) {
        setZones(response.data.zones);
        // If a zone is already selected, update its data
        if (selectedZone) {
          const updated = response.data.zones.find(z => z.district === selectedZone.district);
          if (updated) setSelectedZone(updated);
        }
      }
    } catch (err) {
      console.error(err);
      setError('Failed to fetch cyber zones');
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = (level) => {
    switch (level?.toLowerCase()) {
      case 'critical': return 'risk-critical';
      case 'high': return 'risk-high';
      case 'medium': return 'risk-medium';
      default: return 'risk-low';
    }
  };

  if (loading && zones.length === 0) {
    return (
      <MainLayout>
        <div className="zones-loading">
          <div className="spinner"></div>
          <p>Analyzing Cyber Security Zones...</p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="cyber-zones-page">
        <div className="zones-header">
          <div>
            <h1>🛡️ Cyber Security Zones</h1>
            <p>Geofenced regional zones mapped to Madhya Pradesh districts</p>
          </div>
          <div className="zones-summary-badge">
            <span className="pulse-green"></span>
            Active Geofences: {zones.length} Districts
          </div>
        </div>

        {error && <div className="error-banner">{error}</div>}

        <div className="zones-layout">
          {/* Grid of Zones */}
          <div className="zones-grid-container">
            <h2>Region-based Geofence Registry</h2>
            <div className="zones-grid">
              {zones.map((zone, idx) => {
                const isCritical = zone.risk_level === 'critical';
                return (
                  <motion.div
                    key={zone.district || idx}
                    className={`zone-card ${getRiskClass(zone.risk_level)} ${selectedZone?.district === zone.district ? 'active-card' : ''}`}
                    onClick={() => setSelectedZone(zone)}
                    whileHover={{ y: -4, scale: 1.02 }}
                    transition={{ duration: 0.2 }}
                  >
                    {isCritical && <div className="critical-pulse-overlay"></div>}
                    <div className="zone-card-header">
                      <h3>{zone.zone_name}</h3>
                      <span className={`risk-badge ${zone.risk_level}`}>
                        {zone.risk_level?.toUpperCase()}
                      </span>
                    </div>

                    <div className="zone-metrics">
                      <div className="metric">
                        <span className="metric-label">Risk Index:</span>
                        <span className="metric-value">{zone.risk_score}/100</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">Active Threats:</span>
                        <span className="metric-value count">{zone.threat_count}</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">Incidents:</span>
                        <span className={`metric-value ${zone.active_incidents > 0 ? 'alerting' : ''}`}>
                          {zone.active_incidents}
                        </span>
                      </div>
                    </div>

                    <div className="zone-footer">
                      <span><FiShield /> {zone.asset_count} Assets Protected</span>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>

          {/* Details Drawer / Panel */}
          <div className="zone-details-panel">
            <AnimatePresence mode="wait">
              {selectedZone ? (
                <motion.div
                  key={selectedZone.district}
                  className="details-content"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                >
                  <div className="details-header">
                    <h2>{selectedZone.zone_name} Profile</h2>
                    <p>Protected Infrastructure & Asset Registry</p>
                  </div>

                  <div className="zone-quick-stats">
                    <div className="stat-box">
                      <FiActivity />
                      <h4>Risk Rating</h4>
                      <p className={`value ${selectedZone.risk_level}`}>{selectedZone.risk_score}</p>
                    </div>
                    <div className="stat-box">
                      <FiAlertTriangle />
                      <h4>Incidents</h4>
                      <p className="value">{selectedZone.active_incidents}</p>
                    </div>
                  </div>

                  <div className="assets-section">
                    <h3>🏛️ Registered Assets ({selectedZone.asset_count})</h3>
                    {selectedZone.protected_assets && selectedZone.protected_assets.length > 0 ? (
                      <div className="assets-list">
                        {selectedZone.protected_assets.map((asset, idx) => (
                          <div key={asset._id || idx} className={`asset-list-item ${asset.criticality}`}>
                            <div className="asset-info">
                              <h4>{asset.name}</h4>
                              <span className="asset-type">{asset.type}</span>
                            </div>
                            <span className={`criticality-tag ${asset.criticality}`}>
                              {asset.criticality?.toUpperCase()}
                            </span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="no-assets-msg">No assets registered in this district registry.</p>
                    )}
                  </div>
                </motion.div>
              ) : (
                <div className="no-zone-selected">
                  <FiMapPin size={48} />
                  <h3>Select a Cyber Zone</h3>
                  <p>Click on any district Cyber Zone card to view registered critical infrastructure assets, threat logs, and real-time security postures.</p>
                </div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
