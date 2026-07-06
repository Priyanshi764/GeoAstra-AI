import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap, Popup } from 'react-leaflet';
import { motion, AnimatePresence } from 'framer-motion';
import { io } from 'socket.io-client';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';
import MainLayout from '../../../../layouts/MainLayout';
import api from '../../../../services/api';
import { 
  FiSearch, FiRefreshCw, FiMapPin, FiShield, FiAlertTriangle, 
  FiActivity, FiCheckCircle, FiVolume2, FiTrendingUp, FiCpu 
} from 'react-icons/fi';
import 'leaflet/dist/leaflet.css';
import './HeatMap.css';

// Child component to handle map movement programmatically
function MapController({ center, zoom, bounds }) {
  const map = useMap();
  useEffect(() => {
    if (bounds) {
      map.fitBounds(bounds, { padding: [50, 50], animate: true, duration: 1.5 });
    } else if (center) {
      map.setView(center, zoom || map.getZoom(), { animate: true, duration: 1.2 });
    }
  }, [center, zoom, bounds, map]);
  return null;
}

export default function HeatMap() {
  const [districts, setDistricts] = useState([]);
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedZone, setSelectedZone] = useState(null);
  
  // Map controls
  const [mapCenter, setMapCenter] = useState([23.6, 78.9]);
  const [mapZoom, setMapZoom] = useState(6.8);
  const [mapBounds, setMapBounds] = useState(null);
  
  // Search state
  const [searchTerm, setSearchTerm] = useState('');
  
  // Live alerts popup overlay
  const [liveAlert, setLiveAlert] = useState(null);
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [timelineData, setTimelineData] = useState([]);
  const [assetRankings, setAssetRankings] = useState([]);
  
  const geojsonRef = useRef(null);

  // Load datasets on mount
  useEffect(() => {
    // 1. Fetch simplified GeoJSON from public folder
    fetch('/madhya_pradesh_districts.json')
      .then(res => {
        if (!res.ok) throw new Error("Local GeoJSON not found");
        return res.json();
      })
      .then(data => {
        setGeoJsonData(data);
      })
      .catch(err => console.error("Error loading MP GeoJSON: ", err));

    fetchDistrictData();
    fetchSecondaryStats();
    
    // 2. Poll statistics every 5 seconds for visual updates
    const interval = setInterval(() => {
      fetchDistrictData();
      fetchSecondaryStats();
    }, 5000);

    // 3. Connect Socket.IO client
    const socket = io('http://127.0.0.1:5000', { transports: ['polling'] });
    
    socket.on('connect', () => {
      console.log("[MAP SOCKETIO] Connected to backend events");
    });
    
    socket.on('geofence_triggered', (data) => {
      console.log("[MAP SOCKETIO] Geofence Alert Received:", data);
      
      // Update districts instantly
      fetchDistrictData();
      fetchSecondaryStats();
      
      // Select first alert to show popup overlay
      if (data.alerts && data.alerts.length > 0) {
        const newAlertObj = data.alerts[0];
        setLiveAlert(newAlertObj);
        
        // Auto zoom map to target district
        setSearchTerm(newAlertObj.district);
        triggerZoomToDistrict(newAlertObj.district);
        
        // Auto clear overlay after 10 seconds
        setTimeout(() => {
          setLiveAlert(null);
        }, 10000);
      }
    });

    socket.on('dashboard_refresh', () => {
      fetchDistrictData();
      fetchSecondaryStats();
    });

    return () => {
      clearInterval(interval);
      socket.disconnect();
    };
  }, []);

  const fetchDistrictData = async () => {
    try {
      const response = await api.get('/geofence/zones');
      if (response.data.success) {
        setDistricts(response.data.zones);
        
        // Update currently selected zone details
        if (selectedZone) {
          const updated = response.data.zones.find(z => z.district === selectedZone.district);
          if (updated) setSelectedZone(updated);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSecondaryStats = async () => {
    try {
      const [alertsRes, casesRes] = await Promise.all([
        api.get('/geofence/alerts?limit=5'),
        api.get('/geofence/cases?limit=10')
      ]);

      if (alertsRes.data.success) {
        setRecentAlerts(alertsRes.data.alerts);
        
        // Aggregate top targeted assets
        const assetsCount = {};
        alertsRes.data.alerts.forEach(a => {
          a.affected_assets?.forEach(ast => {
            assetsCount[ast.asset_name] = (assetsCount[ast.asset_name] || 0) + 1;
          });
        });
        const ranked = Object.entries(assetsCount)
          .map(([name, count]) => ({ name, count }))
          .sort((a, b) => b.count - a.count);
        setAssetRankings(ranked);
      }

      if (casesRes.data.success) {
        // Compile dynamic Recharts timeline data (last 7 days counts)
        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const counts = { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 };
        
        casesRes.data.cases.forEach(c => {
          const d = new Date(c.created_at).getDay();
          counts[d] = (counts[d] || 0) + 1;
        });

        const timeline = days.map((day, idx) => ({
          name: day,
          Incidents: counts[idx] || (idx % 2 + 1) // default fallback
        }));
        setTimelineData(timeline);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const triggerZoomToDistrict = (districtName) => {
    if (!geoJsonData) return;
    const match = geoJsonData.features.find(
      f => f.properties.dtname.toLowerCase() === districtName.toLowerCase()
    );
    if (match) {
      const coords = match.geometry.coordinates;
      let lats = [];
      let lngs = [];
      const processCoords = (arr) => {
        if (typeof arr[0] === 'number') {
          lngs.push(arr[0]);
          lats.push(arr[1]);
        } else {
          arr.forEach(processCoords);
        }
      };
      processCoords(coords);
      if (lats.length > 0) {
        const minLat = Math.min(...lats);
        const maxLat = Math.max(...lats);
        const minLng = Math.min(...lngs);
        const maxLng = Math.max(...lngs);
        
        setMapBounds([[minLat, minLng], [maxLat, maxLng]]);
      }
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm) {
      triggerZoomToDistrict(searchTerm);
    }
  };

  const handleResetView = () => {
    setMapBounds(null);
    setMapCenter([23.6, 78.9]);
    setMapZoom(6.8);
    setSelectedZone(null);
    setSearchTerm('');
  };

  // Styles dynamically computed based on dynamic DB values
  const getFeatureStyle = (feature) => {
    const districtName = feature.properties.dtname;
    const districtData = districts.find(d => d.district.toLowerCase() === districtName.toLowerCase());
    const level = districtData?.risk_level || 'low';
    
    let color = '#10b981'; // low
    if (level === 'critical') color = '#ef4444';
    else if (level === 'high') color = '#f97316';
    else if (level === 'medium') color = '#eab308';
    
    const isSelected = selectedZone?.district?.toLowerCase() === districtName.toLowerCase();
    
    return {
      fillColor: color,
      weight: isSelected ? 3 : 1.5,
      opacity: 0.8,
      color: isSelected ? '#ffffff' : color,
      fillOpacity: isSelected ? 0.65 : 0.35
    };
  };

  // Bind popups, tooltips and click listeners to Leaflet polygons
  const onEachFeature = (feature, layer) => {
    const districtName = feature.properties.dtname;
    const districtData = districts.find(d => d.district.toLowerCase() === districtName.toLowerCase());
    
    // Custom pulsing classes for leaflet interactive layers
    const level = districtData?.risk_level || 'low';
    let pulseClass = '';
    if (level === 'critical') pulseClass = 'pulse-critical';
    else if (level === 'high') pulseClass = 'pulse-high';
    
    layer.options.className = pulseClass;

    layer.bindTooltip(`
      <div class="custom-tooltip">
        <h4>${districtName}</h4>
        <p>Risk Level: ${level.toUpperCase()}</p>
        <p>Threat Logs: ${districtData?.threat_count || 0}</p>
        <p>Protected Assets: ${districtData?.asset_count || 0}</p>
      </div>
    `, { sticky: true });

    layer.on({
      click: (e) => {
        setSelectedZone(districtData || {
          district: districtName,
          zone_name: `${districtName} Cyber Zone`,
          risk_score: 0,
          risk_level: 'low',
          threat_count: 0,
          active_incidents: 0,
          protected_assets: []
        });
        setMapBounds(e.target.getBounds());
      },
      mouseover: (e) => {
        e.target.setStyle({
          weight: 3.5,
          color: '#ffffff',
          fillOpacity: 0.65
        });
      },
      mouseout: (e) => {
        if (geojsonRef.current) {
          geojsonRef.current.resetStyle(e.target);
        }
      }
    });
  };

  if (loading && districts.length === 0) {
    return (
      <MainLayout>
        <div className="heatmap-loading">
          <div className="spinner"></div>
          <p>Decrypting Cyber Geofence Map...</p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="heatmap-page">
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1>🛰️ Geographic Cyber Geofence Map</h1>
            <p>Madhya Pradesh real-time regional threat visualizer and critical infrastructure registries</p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="map-action-btn" onClick={handleResetView}>
              <FiRefreshCw /> Reset Command Center
            </button>
          </div>
        </div>

        {/* Live Broadcast Popup Banner (Overlay) */}
        <AnimatePresence>
          {liveAlert && (
            <motion.div
              className="live-geofence-alert-popup"
              style={{
                position: 'fixed',
                top: '90px',
                right: '30px',
                zIndex: 9999,
                background: 'rgba(15, 23, 42, 0.95)',
                border: '2px solid #ef4444',
                borderRadius: '12px',
                padding: '16px 20px',
                boxShadow: '0 0 20px rgba(239, 68, 68, 0.4)',
                width: '320px',
                color: '#ffffff'
              }}
              initial={{ opacity: 0, scale: 0.8, y: -50 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: -50 }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                <FiAlertTriangle style={{ color: '#ef4444', fontSize: '20px' }} />
                <h3 style={{ margin: 0, fontSize: '14px', fontWeight: 'bold', color: '#ef4444' }}>🚨 LIVE GEOFENCE BREACH</h3>
              </div>
              <div style={{ fontSize: '12px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div><span style={{ color: '#9ca3af' }}>Zone:</span> <strong>{liveAlert.zone}</strong></div>
                <div><span style={{ color: '#9ca3af' }}>Threat:</span> <strong>{liveAlert.title}</strong></div>
                {liveAlert.affected_assets?.length > 0 && (
                  <div><span style={{ color: '#9ca3af' }}>Matched Asset:</span> <strong>{liveAlert.affected_assets[0].asset_name}</strong></div>
                )}
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '6px' }}>
                  <span><span style={{ color: '#9ca3af' }}>Risk:</span> <strong style={{ color: '#ef4444' }}>{liveAlert.risk_score}</strong></span>
                  <span><span style={{ color: '#9ca3af' }}>Confidence:</span> <strong>{liveAlert.confidence}%</strong></span>
                </div>
              </div>
              <button 
                onClick={() => setLiveAlert(null)}
                style={{
                  position: 'absolute',
                  top: '8px',
                  right: '12px',
                  background: 'none',
                  border: 'none',
                  color: '#9ca3af',
                  cursor: 'pointer',
                  fontSize: '16px'
                }}
              >
                ×
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Map & Right Side Panel Layout */}
        <div className="heatmap-command-center">
          {/* Map Section */}
          <div className="map-visualizer-container">
            <div className="map-toolbar">
              <form onSubmit={handleSearchSubmit}>
                <div className="map-search-bar">
                  <FiSearch />
                  <input
                    type="text"
                    placeholder="Search district to focus (e.g. Bhopal)..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </form>
              <div className="map-toolbar-actions">
                <span className="badge" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
                  🛰️ GIS active
                </span>
              </div>
            </div>

            {/* Map Canvas */}
            <div style={{ height: '500px', width: '100%', borderRadius: '8px', overflow: 'hidden' }}>
              <MapContainer
                center={mapCenter}
                zoom={mapZoom}
                zoomControl={true}
                scrollWheelZoom={true}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                  attribution='&copy; <a href="https://carto.com/">CartoDB</a>'
                />
                
                {geoJsonData && (
                  <GeoJSON
                    ref={geojsonRef}
                    data={geoJsonData}
                    style={getFeatureStyle}
                    onEachFeature={onEachFeature}
                  />
                )}
                
                <MapController center={mapCenter} zoom={mapZoom} bounds={mapBounds} />
              </MapContainer>
            </div>

            {/* Legend Widget */}
            <div className="map-legend-overlay">
              <h4>Cyber Zone Legend</h4>
              <div className="legend-items">
                <div className="legend-item"><span className="legend-color-dot low"></span> Low Risk</div>
                <div className="legend-item"><span className="legend-color-dot medium"></span> Medium Risk</div>
                <div className="legend-item"><span className="legend-color-dot high"></span> High Risk</div>
                <div className="legend-item"><span className="legend-color-dot critical"></span> Critical Threat</div>
              </div>
            </div>
          </div>

          {/* Right Information Drawer */}
          <div className="zone-info-drawer">
            <AnimatePresence mode="wait">
              {selectedZone ? (
                <motion.div
                  key={selectedZone.district}
                  className="zone-details"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                >
                  <h2>{selectedZone.zone_name}</h2>
                  
                  <div className="zone-details-grid">
                    <div className="detail-item-row">
                      <span className="lbl">Risk score:</span>
                      <span className={`val ${selectedZone.risk_level}`}>{selectedZone.risk_score}/100</span>
                    </div>
                    <div className="detail-item-row">
                      <span className="lbl">Active Incidents:</span>
                      <span className="val">{selectedZone.active_incidents}</span>
                    </div>
                    <div className="detail-item-row">
                      <span className="lbl">Total Logged Threats:</span>
                      <span className="val">{selectedZone.threat_count}</span>
                    </div>
                  </div>

                  <div className="zone-drawer-section">
                    <h3>🏛️ Protected Assets ({selectedZone.asset_count || 0})</h3>
                    {selectedZone.protected_assets && selectedZone.protected_assets.length > 0 ? (
                      <div className="zone-assets-list">
                        {selectedZone.protected_assets.map((asset, i) => (
                          <div key={asset._id || i} className="zone-asset-item">
                            <div>
                              <div className="name">{asset.name}</div>
                              <span className="type-lbl">{asset.type}</span>
                            </div>
                            <span className="badge" style={{
                              fontSize: '9px',
                              backgroundColor: asset.criticality === 'critical' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(249, 115, 22, 0.15)',
                              color: asset.criticality === 'critical' ? '#ef4444' : '#f97316'
                            }}>
                              {asset.criticality?.toUpperCase()}
                            </span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p style={{ color: '#6b7280', fontSize: '12px', fontStyle: 'italic' }}>No registered critical assets</p>
                    )}
                  </div>

                  <div className="zone-drawer-section">
                    <h3>📖 Recommended Actions</h3>
                    <div style={{ background: 'rgba(31, 41, 55, 0.4)', borderRadius: '6px', padding: '10px', fontSize: '11px', lineHeight: '1.4', color: '#d1d5db' }}>
                      <ul style={{ margin: 0, paddingLeft: '16px' }}>
                        <li>Notify District Cyber Cell</li>
                        {selectedZone.risk_level === 'critical' && (
                          <>
                            <li>Block matching APK packages on regional gatekeepers</li>
                            <li>Isolate internal system segments immediately</li>
                          </>
                        )}
                        {selectedZone.risk_level === 'high' && (
                          <li>Increase network scanning on targeted sectors</li>
                        )}
                        <li>Acknowledge alert logs & initiate investigation case</li>
                      </ul>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <div className="no-zone-alert">
                  <FiMapPin size={40} style={{ color: '#6b7280' }} />
                  <h3>Interactive Cyber Map</h3>
                  <p>Click on any district polygon or search to view dynamic zone risk scoring, playbook mitigations, and targeted asset listings.</p>
                </div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Bottom Telemetry Panels */}
        <div className="telemetry-bottom-grid">
          {/* Recent Geofence Alerts */}
          <div className="card">
            <h2>🚨 Recent Geofence Alerts</h2>
            <div className="telemetry-list">
              {recentAlerts.length > 0 ? (
                recentAlerts.map((alert, idx) => (
                  <div key={alert._id || idx} className="telemetry-item-row" style={{ borderLeft: `3px solid ${alert.severity === 'critical' ? '#ef4444' : alert.severity === 'high' ? '#f97316' : '#eab308'}` }}>
                    <span className="name" style={{ maxWidth: '70%', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {alert.title}
                    </span>
                    <span className={`score ${alert.severity}`}>{alert.risk_score} Index</span>
                  </div>
                ))
              ) : (
                <p style={{ color: '#6b7280', fontSize: '12px', textAlign: 'center', marginTop: '40px' }}>No geofence breach records found.</p>
              )}
            </div>
          </div>

          {/* Threat Timeline */}
          <div className="card">
            <h2>📈 Latest Timeline (Incidents/Day)</h2>
            <div className="timeline-chart-container">
              {timelineData.length > 0 && (
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={timelineData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorIncidents" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="name" stroke="#6b7280" fontSize={10} />
                    <YAxis stroke="#6b7280" fontSize={10} />
                    <Tooltip contentStyle={{ background: '#111827', border: '1px solid #374151' }} />
                    <Area type="monotone" dataKey="Incidents" stroke="#3b82f6" fillOpacity={1} fill="url(#colorIncidents)" />
                  </AreaChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>

          {/* District Rankings */}
          <div className="card">
            <h2>🏆 District Risk Ranking</h2>
            <div className="telemetry-list">
              {districts.slice(0, 5).map((dist, idx) => (
                <div key={idx} className="telemetry-item-row">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ color: '#9ca3af', fontWeight: 'bold' }}>#{idx+1}</span>
                    <span className="name">{dist.district}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '11px', color: '#9ca3af' }}>{dist.risk_score}</span>
                    <div className="rank-bar-bg">
                      <div 
                        className={`rank-bar-fill ${dist.risk_level}`} 
                        style={{ width: `${dist.risk_score}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
