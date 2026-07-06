import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MainLayout from '../../layouts/MainLayout';
import { FiTrendingUp, FiBarChart2, FiPieChart, FiCalendar } from 'react-icons/fi';
import './Analytics.css';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeRange, setTimeRange] = useState('30d');

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE_URL}/dashboard/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data.stats);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch analytics');
      console.error('Analytics error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="analytics-loading">
          <div className="spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="analytics">
        <div className="analytics-header">
          <div>
            <h1>Security Analytics</h1>
            <p>Real-time threat intelligence and security metrics</p>
          </div>
          <div className="time-range-selector">
            <button 
              className={timeRange === '7d' ? 'active' : ''} 
              onClick={() => setTimeRange('7d')}
            >
              7 Days
            </button>
            <button 
              className={timeRange === '30d' ? 'active' : ''} 
              onClick={() => setTimeRange('30d')}
            >
              30 Days
            </button>
            <button 
              className={timeRange === '90d' ? 'active' : ''} 
              onClick={() => setTimeRange('90d')}
            >
              90 Days
            </button>
          </div>
        </div>

        {error && <div className="error-banner">{error}</div>}

        {/* Key Metrics */}
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon alert">⚠️</div>
            <div className="metric-content">
              <p className="metric-label">Total Alerts</p>
              <p className="metric-value">{stats?.alerts?.total || 0}</p>
              <p className="metric-change">
                {stats?.alerts?.last_24h || 0} in last 24h
              </p>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon critical">🔴</div>
            <div className="metric-content">
              <p className="metric-label">Critical Alerts</p>
              <p className="metric-value">{stats?.alerts?.critical || 0}</p>
              <p className="metric-change">
                {Math.round((stats?.alerts?.critical / (stats?.alerts?.total || 1)) * 100)}% of total
              </p>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon threat">🛡️</div>
            <div className="metric-content">
              <p className="metric-label">Total Threats</p>
              <p className="metric-value">{stats?.threats?.total || 0}</p>
              <p className="metric-change">
                {stats?.threats?.high_risk || 0} high-risk
              </p>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon asset">🏢</div>
            <div className="metric-content">
              <p className="metric-label">Protected Assets</p>
              <p className="metric-value">{stats?.assets?.total || 0}</p>
              <p className="metric-change">
                {stats?.assets?.critical || 0} critical
              </p>
            </div>
          </div>
        </div>

        {/* Analytics Sections */}
        <div className="analytics-grid">
          {/* Threat Types */}
          <div className="analytics-card">
            <div className="card-header">
              <h3>
                <FiBarChart2 /> Threat Types Distribution
              </h3>
              <span className="card-icon">📊</span>
            </div>
            <div className="chart-container">
              {stats?.coverage?.threat_types && stats.coverage.threat_types.length > 0 ? (
                <div className="threat-types-list">
                  {stats.coverage.threat_types.map((item, idx) => (
                    <div key={idx} className="threat-type-item">
                      <div className="threat-type-bar">
                        <span className="threat-name">{item._id}</span>
                        <div className="bar-container">
                          <div 
                            className="bar"
                            style={{
                              width: `${(item.count / (stats.coverage.threat_types[0]?.count || 1)) * 100}%`
                            }}
                          ></div>
                        </div>
                        <span className="threat-count">{item.count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="no-data">No threat data available</p>
              )}
            </div>
          </div>

          {/* Alert Severity Breakdown */}
          <div className="analytics-card">
            <div className="card-header">
              <h3>
                <FiPieChart /> Alert Severity Levels
              </h3>
              <span className="card-icon">🎯</span>
            </div>
            <div className="severity-breakdown">
              <div className="severity-item critical">
                <span className="severity-dot"></span>
                <span className="severity-label">Critical</span>
                <span className="severity-count">{stats?.alerts?.critical || 0}</span>
              </div>
              <div className="severity-item high">
                <span className="severity-dot"></span>
                <span className="severity-label">High</span>
                <span className="severity-count">{stats?.alerts?.high || 0}</span>
              </div>
              <div className="severity-item medium">
                <span className="severity-dot"></span>
                <span className="severity-label">Medium</span>
                <span className="severity-count">{stats?.alerts?.medium || 0}</span>
              </div>
              <div className="severity-item low">
                <span className="severity-dot"></span>
                <span className="severity-label">Low</span>
                <span className="severity-count">{stats?.alerts?.low || 0}</span>
              </div>
            </div>
          </div>

          {/* Top Organizations at Risk */}
          <div className="analytics-card full-width">
            <div className="card-header">
              <h3>
                <FiTrendingUp /> Top Organizations Under Threat
              </h3>
              <span className="card-icon">🎪</span>
            </div>
            <div className="organizations-list">
              {stats?.coverage?.top_organizations && stats.coverage.top_organizations.length > 0 ? (
                stats.coverage.top_organizations.slice(0, 8).map((org, idx) => (
                  <div key={idx} className="org-item">
                    <div className="org-rank">{idx + 1}</div>
                    <div className="org-info">
                      <p className="org-name">{org._id}</p>
                      <div className="org-bar">
                        <div 
                          className="org-bar-fill"
                          style={{
                            width: `${(org.count / (stats.coverage.top_organizations[0]?.count || 1)) * 100}%`
                          }}
                        ></div>
                      </div>
                    </div>
                    <p className="org-count">{org.count} threats</p>
                  </div>
                ))
              ) : (
                <p className="no-data">No organization data available</p>
              )}
            </div>
          </div>

          {/* Top Districts */}
          <div className="analytics-card full-width">
            <div className="card-header">
              <h3>
                <FiCalendar /> Geographic Threat Distribution
              </h3>
              <span className="card-icon">🗺️</span>
            </div>
            <div className="districts-grid">
              {stats?.coverage?.top_districts && stats.coverage.top_districts.length > 0 ? (
                stats.coverage.top_districts.map((district, idx) => (
                  <div key={idx} className="district-card">
                    <p className="district-name">{district._id}</p>
                    <p className="district-count">{district.count} threats</p>
                    <p className="district-risk">
                      Avg Risk: {district.avg_risk?.toFixed(1) || 0}
                    </p>
                    <div className="district-bar">
                      <div 
                        className="district-bar-fill"
                        style={{
                          width: `${(district.count / (stats.coverage.top_districts[0]?.count || 1)) * 100}%`
                        }}
                      ></div>
                    </div>
                  </div>
                ))
              ) : (
                <p className="no-data">No district data available</p>
              )}
            </div>
          </div>

          {/* Threat Categories */}
          <div className="analytics-card full-width">
            <div className="card-header">
              <h3>Threat Categories</h3>
              <span className="card-icon">📋</span>
            </div>
            <div className="categories-table">
              <table>
                <tbody>
                  {stats?.coverage?.threat_categories && stats.coverage.threat_categories.length > 0 ? (
                    stats.coverage.threat_categories.map((cat, idx) => (
                      <tr key={idx}>
                        <td className="cat-name">{cat._id}</td>
                        <td className="cat-count">{cat.count}</td>
                        <td className="cat-bar">
                          <div className="progress-bar">
                            <div 
                              className="progress-fill"
                              style={{
                                width: `${(cat.count / (stats.coverage.threat_categories[0]?.count || 1)) * 100}%`
                              }}
                            ></div>
                          </div>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr><td colSpan="3" className="no-data">No category data available</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
