import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MainLayout from '../../layouts/MainLayout';
import { FiSearch, FiFilter, FiChevronDown, FiDownload } from 'react-icons/fi';
import './Investigation.css';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default function Investigation() {
  const [threats, setThreats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedThreat, setSelectedThreat] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    category: '',
    minRisk: 0,
    district: ''
  });
  const [expandedThreat, setExpandedThreat] = useState(null);

  useEffect(() => {
    fetchThreats();
  }, [filters]);

  const fetchThreats = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const params = new URLSearchParams();
      
      if (filters.category) params.append('category', filters.category);
      if (filters.minRisk > 0) params.append('min_risk', filters.minRisk);
      if (filters.district) params.append('district', filters.district);
      
      params.append('limit', 50);

      const response = await axios.get(`${API_BASE_URL}/threats?${params.toString()}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setThreats(response.data.threats || []);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch threats');
      console.error('Investigation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityBadge = (riskScore) => {
    if (riskScore >= 8) return 'critical';
    if (riskScore >= 6) return 'high';
    if (riskScore >= 4) return 'medium';
    return 'low';
  };

  const getSeverityLabel = (riskScore) => {
    if (riskScore >= 8) return 'Critical';
    if (riskScore >= 6) return 'High';
    if (riskScore >= 4) return 'Medium';
    return 'Low';
  };

  const filteredThreats = threats.filter(threat => {
    const searchLower = searchTerm.toLowerCase();
    return (
      threat.threat_type?.toLowerCase().includes(searchLower) ||
      threat.category?.toLowerCase().includes(searchLower) ||
      threat.summary?.toLowerCase().includes(searchLower) ||
      threat.organizations?.some(org => org.toLowerCase().includes(searchLower))
    );
  });

  const handleDownloadReport = (threat) => {
    const report = `
THREAT INVESTIGATION REPORT
============================
Generated: ${new Date().toLocaleString()}

THREAT DETAILS
==============
ID: ${threat._id}
Type: ${threat.threat_type}
Category: ${threat.category}
Risk Score: ${threat.risk_score}/10
Confidence: ${threat.confidence}%
Status: ${threat.status || 'Active'}

SUMMARY
${threat.summary}

AFFECTED ENTITIES
=================
Organizations: ${threat.organizations?.join(', ') || 'N/A'}
Districts: ${threat.districts?.join(', ') || 'N/A'}
State: ${threat.state || 'N/A'}

THREAT ANALYSIS
===============
Threat Actors: ${threat.threat_actors?.join(', ') || 'N/A'}
Attack Vector: ${threat.attack_vector || 'N/A'}
Malware Family: ${threat.malware_family || 'N/A'}

RECOMMENDATIONS
${threat.recommendation}

MITRE ATT&CK
============
${threat.mitre_attack?.join(', ') || 'N/A'}

INDICATORS OF COMPROMISE (IoCs)
===============================
Domains: ${threat.iocs?.domains?.join(', ') || 'N/A'}
IP Addresses: ${threat.iocs?.ips?.join(', ') || 'N/A'}
URLs: ${threat.iocs?.urls?.join(', ') || 'N/A'}
Email Addresses: ${threat.iocs?.emails?.join(', ') || 'N/A'}
File Hashes: ${threat.iocs?.hashes?.join(', ') || 'N/A'}
`;

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(report));
    element.setAttribute('download', `threat_report_${threat._id}.txt`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="investigation-loading">
          <div className="spinner"></div>
          <p>Loading threats...</p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="investigation">
        <div className="investigation-header">
          <div>
            <h1>Threat Investigation</h1>
            <p>Deep dive analysis of detected security threats</p>
          </div>
        </div>

        {error && <div className="error-banner">{error}</div>}

        {/* Search and Filters */}
        <div className="search-filter-section">
          <div className="search-box">
            <FiSearch />
            <input
              type="text"
              placeholder="Search threats by type, category, organization..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="filter-section">
            <select
              value={filters.category}
              onChange={(e) => setFilters({...filters, category: e.target.value})}
              className="filter-select"
            >
              <option value="">All Categories</option>
              <option value="Malware">Malware</option>
              <option value="Phishing">Phishing</option>
              <option value="Credential Leak">Credential Leak</option>
              <option value="Banking Malware">Banking Malware</option>
              <option value="Ransomware">Ransomware</option>
              <option value="Investment Scam">Investment Scam</option>
              <option value="Identity Fraud">Identity Fraud</option>
              <option value="Fake APK">Fake APK</option>
              <option value="Data Breach">Data Breach</option>
              <option value="Money Laundering">Money Laundering</option>
              <option value="Financial Fraud">Financial Fraud</option>
            </select>

            <select
              value={filters.minRisk}
              onChange={(e) => setFilters({...filters, minRisk: parseInt(e.target.value)})}
              className="filter-select"
            >
              <option value="0">All Risk Levels</option>
              <option value="4">Medium & Above</option>
              <option value="6">High & Above</option>
              <option value="8">Critical Only</option>
            </select>

            <select
              value={filters.district}
              onChange={(e) => setFilters({...filters, district: e.target.value})}
              className="filter-select"
            >
              <option value="">All Districts</option>
              <option value="Bhopal">Bhopal</option>
              <option value="Indore">Indore</option>
              <option value="Jabalpur">Jabalpur</option>
              <option value="Gwalior">Gwalior</option>
              <option value="Ujjain">Ujjain</option>
              <option value="Sagar">Sagar</option>
              <option value="Nagpur">Nagpur</option>
              <option value="Ratlam">Ratlam</option>
            </select>
          </div>
        </div>

        {/* Threats List */}
        <div className="threats-section">
          <div className="section-header">
            <h2>Detected Threats ({filteredThreats.length})</h2>
            <span className="threat-count">{filteredThreats.length} found</span>
          </div>

          {filteredThreats.length > 0 ? (
            <div className="threats-list">
              {filteredThreats.map((threat) => (
                <div 
                  key={threat._id}
                  className={`threat-item ${expandedThreat === threat._id ? 'expanded' : ''}`}
                >
                  <div 
                    className="threat-header-row"
                    onClick={() => setExpandedThreat(expandedThreat === threat._id ? null : threat._id)}
                  >
                    <div className="threat-basic-info">
                      <div className="threat-icon">🔍</div>
                      <div className="threat-summary">
                        <h3>{threat.threat_type}</h3>
                        <p>{threat.summary?.substring(0, 80)}...</p>
                      </div>
                    </div>

                    <div className="threat-meta">
                      <div className={`severity-badge ${getSeverityBadge(threat.risk_score)}`}>
                        {getSeverityLabel(threat.risk_score)}
                      </div>
                      <div className="risk-score">
                        <span className="score">{threat.risk_score}</span>
                        <span className="label">/10</span>
                      </div>
                      <button className="expand-btn">
                        <FiChevronDown />
                      </button>
                    </div>
                  </div>

                  {expandedThreat === threat._id && (
                    <div className="threat-details">
                      <div className="details-grid">
                        <div className="detail-section">
                          <h4>General Information</h4>
                          <div className="detail-row">
                            <span className="label">Category:</span>
                            <span className="value">{threat.category}</span>
                          </div>
                          <div className="detail-row">
                            <span className="label">Confidence:</span>
                            <span className="value">{threat.confidence}%</span>
                          </div>
                          <div className="detail-row">
                            <span className="label">Status:</span>
                            <span className="value">{threat.status || 'Active'}</span>
                          </div>
                          <div className="detail-row">
                            <span className="label">Created:</span>
                            <span className="value">{new Date(threat.created_at).toLocaleDateString()}</span>
                          </div>
                        </div>

                        <div className="detail-section">
                          <h4>Impact Analysis</h4>
                          <div className="detail-row">
                            <span className="label">Affected Organizations:</span>
                            <span className="value">{threat.organizations?.length || 0}</span>
                          </div>
                          <div className="detail-row">
                            <span className="label">Affected Districts:</span>
                            <span className="value">{threat.districts?.join(', ') || 'N/A'}</span>
                          </div>
                          <div className="detail-row">
                            <span className="label">State:</span>
                            <span className="value">{threat.state}</span>
                          </div>
                        </div>

                        <div className="detail-section">
                          <h4>Threat Attribution</h4>
                          <div className="detail-row">
                            <span className="label">Threat Actors:</span>
                            <span className="value">{threat.threat_actors?.join(', ') || 'Unknown'}</span>
                          </div>
                          <div className="detail-row">
                            <span className="label">Attack Vector:</span>
                            <span className="value">{threat.attack_vector || 'N/A'}</span>
                          </div>
                          <div className="detail-row">
                            <span className="label">Malware Family:</span>
                            <span className="value">{threat.malware_family || 'N/A'}</span>
                          </div>
                        </div>
                      </div>

                      <div className="detail-section full">
                        <h4>Summary</h4>
                        <p className="summary-text">{threat.summary}</p>
                      </div>

                      <div className="detail-section full">
                        <h4>Recommendation</h4>
                        <p className="recommendation-text">{threat.recommendation}</p>
                      </div>

                      <div className="detail-section full">
                        <h4>MITRE ATT&CK Techniques</h4>
                        <div className="techniques-list">
                          {threat.mitre_attack?.map((tech, idx) => (
                            <span key={idx} className="technique-tag">{tech}</span>
                          ))}
                        </div>
                      </div>

                      <div className="detail-section full">
                        <h4>Indicators of Compromise (IoCs)</h4>
                        <div className="iocs-grid">
                          {threat.iocs?.domains && threat.iocs.domains.length > 0 && (
                            <div className="ioc-group">
                              <span className="ioc-label">Domains:</span>
                              <span className="ioc-values">{threat.iocs.domains.join(', ')}</span>
                            </div>
                          )}
                          {threat.iocs?.ips && threat.iocs.ips.length > 0 && (
                            <div className="ioc-group">
                              <span className="ioc-label">IPs:</span>
                              <span className="ioc-values">{threat.iocs.ips.join(', ')}</span>
                            </div>
                          )}
                          {threat.iocs?.urls && threat.iocs.urls.length > 0 && (
                            <div className="ioc-group">
                              <span className="ioc-label">URLs:</span>
                              <span className="ioc-values">{threat.iocs.urls.join(', ')}</span>
                            </div>
                          )}
                          {threat.iocs?.emails && threat.iocs.emails.length > 0 && (
                            <div className="ioc-group">
                              <span className="ioc-label">Emails:</span>
                              <span className="ioc-values">{threat.iocs.emails.join(', ')}</span>
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="details-footer">
                        <button 
                          className="download-btn"
                          onClick={() => handleDownloadReport(threat)}
                        >
                          <FiDownload /> Download Report
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-threats">
              <p>No threats found matching your criteria</p>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
}
