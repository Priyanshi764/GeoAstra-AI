import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import MainLayout from '../../layouts/MainLayout';
import { AuthContext } from '../../context/AuthContext';
import { FiSave, FiLogOut, FiEye, FiEyeOff, FiMail, FiUser, FiBell, FiLock, FiShield } from 'react-icons/fi';
import './Settings.css';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default function Settings() {
  const { logout, user } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('profile');
  const [message, setMessage] = useState({ type: '', text: '' });
  const [showPassword, setShowPassword] = useState(false);

  // Profile State
  const [profileData, setProfileData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    role: user?.role || 'officer',
    organization: user?.organization || ''
  });

  // Notification Settings State
  const [notificationSettings, setNotificationSettings] = useState({
    emailAlerts: true,
    criticalOnly: false,
    dailyDigest: true,
    weeklyReport: true,
    incidentNotifications: true
  });

  // Security Settings State
  const [securitySettings, setSecuritySettings] = useState({
    twoFactorEnabled: false,
    sessionTimeout: 30,
    ipRestriction: '',
    activityLogging: true
  });

  // Password Change State
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // Threat Settings State
  const [threatSettings, setThreatSettings] = useState({
    minRiskScore: 5,
    autoIncidentCreation: true,
    threatIntelSources: ['internal', 'certin'],
    analysisDepth: 'standard'
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE_URL}/user/settings`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.success) {
        if (response.data.settings.notifications) {
          setNotificationSettings(response.data.settings.notifications);
        }
        if (response.data.settings.security) {
          setSecuritySettings(response.data.settings.security);
        }
        if (response.data.settings.threats) {
          setThreatSettings(response.data.settings.threats);
        }
      }
    } catch (err) {
      // Settings not found, use defaults
      console.log('Using default settings');
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 3000);
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/user/update-profile`,
        profileData,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.success) {
        showMessage('success', 'Profile updated successfully');
      }
    } catch (err) {
      showMessage('error', err.response?.data?.message || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      showMessage('error', 'Passwords do not match');
      return;
    }

    if (passwordData.newPassword.length < 8) {
      showMessage('error', 'Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/user/change-password`,
        passwordData,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.success) {
        setPasswordData({
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        });
        showMessage('success', 'Password changed successfully');
      }
    } catch (err) {
      showMessage('error', err.response?.data?.message || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  const handleNotificationUpdate = async () => {
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/user/settings`,
        { notifications: notificationSettings },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.success) {
        showMessage('success', 'Notification settings saved');
      }
    } catch (err) {
      showMessage('error', 'Failed to save settings');
    } finally {
      setLoading(false);
    }
  };

  const handleSecurityUpdate = async () => {
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/user/settings`,
        { security: securitySettings },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.success) {
        showMessage('success', 'Security settings saved');
      }
    } catch (err) {
      showMessage('error', 'Failed to save security settings');
    } finally {
      setLoading(false);
    }
  };

  const handleThreatUpdate = async () => {
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE_URL}/user/settings`,
        { threats: threatSettings },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.success) {
        showMessage('success', 'Threat settings saved');
      }
    } catch (err) {
      showMessage('error', 'Failed to save threat settings');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      logout();
    }
  };

  return (
    <MainLayout>
      <div className="settings">
        <div className="settings-header">
          <div>
            <h1>Settings & Configuration</h1>
            <p>Manage your account, preferences, and system settings</p>
          </div>
        </div>

        {message.text && (
          <div className={`message-banner ${message.type}`}>
            {message.type === 'success' ? '✅' : '⚠️'} {message.text}
          </div>
        )}

        <div className="settings-container">
          {/* Sidebar Tabs */}
          <div className="settings-sidebar">
            <button
              className={`tab-link ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              <FiUser /> Profile
            </button>
            <button
              className={`tab-link ${activeTab === 'security' ? 'active' : ''}`}
              onClick={() => setActiveTab('security')}
            >
              <FiLock /> Security
            </button>
            <button
              className={`tab-link ${activeTab === 'notifications' ? 'active' : ''}`}
              onClick={() => setActiveTab('notifications')}
            >
              <FiBell /> Notifications
            </button>
            <button
              className={`tab-link ${activeTab === 'threats' ? 'active' : ''}`}
              onClick={() => setActiveTab('threats')}
            >
              <FiShield /> Threat Settings
            </button>
            <div className="sidebar-divider"></div>
            <button
              className="tab-link logout"
              onClick={handleLogout}
            >
              <FiLogOut /> Logout
            </button>
          </div>

          {/* Main Content */}
          <div className="settings-content">
            {/* Profile Tab */}
            {activeTab === 'profile' && (
              <div className="settings-panel">
                <h2>Profile Settings</h2>
                <form onSubmit={handleProfileUpdate}>
                  <div className="form-grid-2col">
                    <div className="form-group">
                      <label>Full Name</label>
                      <input
                        type="text"
                        value={profileData.name}
                        onChange={(e) => setProfileData({...profileData, name: e.target.value})}
                        placeholder="Enter your full name"
                      />
                    </div>

                    <div className="form-group">
                      <label>Organization</label>
                      <input
                        type="text"
                        value={profileData.organization}
                        onChange={(e) => setProfileData({...profileData, organization: e.target.value})}
                        placeholder="Your organization name"
                      />
                    </div>
                  </div>

                  <div className="form-grid-2col">
                    <div className="form-group">
                      <label>Email Address</label>
                      <div className="input-group disabled-input-group">
                        <FiMail />
                        <input
                          type="email"
                          value={profileData.email}
                          disabled
                          placeholder="Your email address"
                        />
                      </div>
                      <p className="help-text">Email cannot be changed</p>
                    </div>

                    <div className="form-group">
                      <label>Role</label>
                      <select 
                        value={profileData.role}
                        onChange={(e) => setProfileData({...profileData, role: e.target.value})}
                        disabled
                        className="disabled-select"
                      >
                        <option value="officer">Security Officer</option>
                        <option value="analyst">Analyst</option>
                        <option value="admin">Administrator</option>
                      </select>
                      <p className="help-text">Role is managed by administrators</p>
                    </div>
                  </div>

                  <button type="submit" className="btn-primary" disabled={loading}>
                    <FiSave /> {loading ? 'Saving...' : 'Save Profile'}
                  </button>
                </form>
              </div>
            )}

            {/* Security Tab */}
            {activeTab === 'security' && (
              <div className="settings-panel">
                <h2>Security Settings</h2>

                {/* Password Change Section */}
                <div className="settings-section">
                  <h3>Change Password</h3>
                  <form onSubmit={handlePasswordChange}>
                    <div className="form-grid-2col">
                      <div className="form-group">
                        <label>Current Password</label>
                        <div className="password-input">
                          <input
                            type={showPassword ? 'text' : 'password'}
                            value={passwordData.currentPassword}
                            onChange={(e) => setPasswordData({...passwordData, currentPassword: e.target.value})}
                            placeholder="Enter current password"
                          />
                          <button
                            type="button"
                            className="toggle-password"
                            onClick={() => setShowPassword(!showPassword)}
                          >
                            {showPassword ? <FiEyeOff /> : <FiEye />}
                          </button>
                        </div>
                      </div>

                      <div className="form-group">
                        <label>New Password</label>
                        <div className="password-input">
                          <input
                            type={showPassword ? 'text' : 'password'}
                            value={passwordData.newPassword}
                            onChange={(e) => setPasswordData({...passwordData, newPassword: e.target.value})}
                            placeholder="Enter new password"
                          />
                        </div>
                        <p className="help-text">At least 8 characters required</p>
                      </div>
                    </div>

                    <div className="form-group" style={{ maxWidth: 'calc(50% - 12px)' }}>
                      <label>Confirm Password</label>
                      <div className="password-input">
                        <input
                          type={showPassword ? 'text' : 'password'}
                          value={passwordData.confirmPassword}
                          onChange={(e) => setPasswordData({...passwordData, confirmPassword: e.target.value})}
                          placeholder="Confirm new password"
                        />
                      </div>
                    </div>

                    <button type="submit" className="btn-primary" disabled={loading}>
                      <FiLock /> {loading ? 'Updating...' : 'Update Password'}
                    </button>
                  </form>
                </div>

                {/* Security Options */}
                <div className="settings-section">
                  <h3>Security Options</h3>
                  
                  <div className="toggle-switch-container">
                    <div className="toggle-info">
                      <span className="toggle-label-text">Enable Two-Factor Authentication</span>
                      <p className="help-text">Adds an extra layer of security to your account</p>
                    </div>
                    <label className="switch">
                      <input
                        type="checkbox"
                        checked={securitySettings.twoFactorEnabled}
                        onChange={(e) => setSecuritySettings({...securitySettings, twoFactorEnabled: e.target.checked})}
                      />
                      <span className="slider round"></span>
                    </label>
                  </div>

                  <div className="form-grid-2col" style={{ marginTop: '20px' }}>
                    <div className="form-group">
                      <label>Session Timeout (minutes)</label>
                      <input
                        type="number"
                        min="5"
                        max="480"
                        value={securitySettings.sessionTimeout}
                        onChange={(e) => setSecuritySettings({...securitySettings, sessionTimeout: parseInt(e.target.value)})}
                      />
                      <p className="help-text">Auto-logout after inactivity</p>
                    </div>

                    <div className="form-group">
                      <label>IP Whitelist (comma-separated)</label>
                      <input
                        type="text"
                        value={securitySettings.ipRestriction}
                        onChange={(e) => setSecuritySettings({...securitySettings, ipRestriction: e.target.value})}
                        placeholder="e.g., 192.168.1.1, 10.0.0.0/8"
                      />
                      <p className="help-text">Leave blank to allow all IPs</p>
                    </div>
                  </div>

                  <div className="toggle-switch-container" style={{ marginTop: '16px' }}>
                    <div className="toggle-info">
                      <span className="toggle-label-text">Enable Activity Logging</span>
                      <p className="help-text">Log all your account activities for audit</p>
                    </div>
                    <label className="switch">
                      <input
                        type="checkbox"
                        checked={securitySettings.activityLogging}
                        onChange={(e) => setSecuritySettings({...securitySettings, activityLogging: e.target.checked})}
                      />
                      <span className="slider round"></span>
                    </label>
                  </div>

                  <button 
                    type="button" 
                    className="btn-primary"
                    onClick={handleSecurityUpdate}
                    disabled={loading}
                    style={{ marginTop: '20px' }}
                  >
                    <FiSave /> {loading ? 'Saving...' : 'Save Security Settings'}
                  </button>
                </div>
              </div>
            )}

            {/* Notifications Tab */}
            {activeTab === 'notifications' && (
              <div className="settings-panel">
                <h2>Notification Preferences</h2>

                <div className="toggle-switch-container">
                  <div className="toggle-info">
                    <span className="toggle-label-text">Email Alerts</span>
                    <p className="help-text">Receive email notifications for new threats</p>
                  </div>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={notificationSettings.emailAlerts}
                      onChange={(e) => setNotificationSettings({...notificationSettings, emailAlerts: e.target.checked})}
                    />
                    <span className="slider round"></span>
                  </label>
                </div>

                <div className={`toggle-switch-container ${!notificationSettings.emailAlerts ? 'disabled-switch-row' : ''}`}>
                  <div className="toggle-info">
                    <span className="toggle-label-text">Critical Alerts Only</span>
                    <p className="help-text">Only send notifications for critical threats</p>
                  </div>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={notificationSettings.criticalOnly}
                      onChange={(e) => setNotificationSettings({...notificationSettings, criticalOnly: e.target.checked})}
                      disabled={!notificationSettings.emailAlerts}
                    />
                    <span className="slider round"></span>
                  </label>
                </div>

                <div className="toggle-switch-container">
                  <div className="toggle-info">
                    <span className="toggle-label-text">Daily Digest</span>
                    <p className="help-text">Send daily summary email at 9:00 AM</p>
                  </div>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={notificationSettings.dailyDigest}
                      onChange={(e) => setNotificationSettings({...notificationSettings, dailyDigest: e.target.checked})}
                    />
                    <span className="slider round"></span>
                  </label>
                </div>

                <div className="toggle-switch-container">
                  <div className="toggle-info">
                    <span className="toggle-label-text">Weekly Report</span>
                    <p className="help-text">Receive weekly threat summary every Monday</p>
                  </div>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={notificationSettings.weeklyReport}
                      onChange={(e) => setNotificationSettings({...notificationSettings, weeklyReport: e.target.checked})}
                    />
                    <span className="slider round"></span>
                  </label>
                </div>

                <div className="toggle-switch-container">
                  <div className="toggle-info">
                    <span className="toggle-label-text">Incident Notifications</span>
                    <p className="help-text">Instant notification for security incidents</p>
                  </div>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={notificationSettings.incidentNotifications}
                      onChange={(e) => setNotificationSettings({...notificationSettings, incidentNotifications: e.target.checked})}
                    />
                    <span className="slider round"></span>
                  </label>
                </div>

                <button 
                  type="button" 
                  className="btn-primary"
                  onClick={handleNotificationUpdate}
                  disabled={loading}
                  style={{ marginTop: '20px' }}
                >
                  <FiSave /> {loading ? 'Saving...' : 'Save Preferences'}
                </button>
              </div>
            )}

            {/* Threat Settings Tab */}
            {activeTab === 'threats' && (
              <div className="settings-panel">
                <h2>Threat Analysis Settings</h2>

                <div className="form-group">
                  <label>Minimum Risk Score for Alerts</label>
                  <div className="slider-group">
                    <input
                      type="range"
                      min="0"
                      max="10"
                      step="0.5"
                      value={threatSettings.minRiskScore}
                      onChange={(e) => setThreatSettings({...threatSettings, minRiskScore: parseFloat(e.target.value)})}
                    />
                    <span className="slider-value">{threatSettings.minRiskScore.toFixed(1)} / 10</span>
                  </div>
                  <p className="help-text">Only threats with risk score above this will trigger active alerts</p>
                </div>

                <div className="toggle-switch-container">
                  <div className="toggle-info">
                    <span className="toggle-label-text">Auto Create Incidents for Critical Threats</span>
                    <p className="help-text">Automatically create incident tickets for critical threats (8+)</p>
                  </div>
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={threatSettings.autoIncidentCreation}
                      onChange={(e) => setThreatSettings({...threatSettings, autoIncidentCreation: e.target.checked})}
                    />
                    <span className="slider round"></span>
                  </label>
                </div>

                <div className="form-group" style={{ marginTop: '20px' }}>
                  <label>Threat Intelligence Feeds</label>
                  <div className="checkbox-pill-group">
                    <label className={`checkbox-pill ${threatSettings.threatIntelSources.includes('internal') ? 'active' : ''}`}>
                      <input
                        type="checkbox"
                        checked={threatSettings.threatIntelSources.includes('internal')}
                        onChange={(e) => {
                          const sources = e.target.checked
                            ? [...threatSettings.threatIntelSources, 'internal']
                            : threatSettings.threatIntelSources.filter(s => s !== 'internal');
                          setThreatSettings({...threatSettings, threatIntelSources: sources});
                        }}
                      />
                      <span>Internal Database</span>
                    </label>
                    <label className={`checkbox-pill ${threatSettings.threatIntelSources.includes('certin') ? 'active' : ''}`}>
                      <input
                        type="checkbox"
                        checked={threatSettings.threatIntelSources.includes('certin')}
                        onChange={(e) => {
                          const sources = e.target.checked
                            ? [...threatSettings.threatIntelSources, 'certin']
                            : threatSettings.threatIntelSources.filter(s => s !== 'certin');
                          setThreatSettings({...threatSettings, threatIntelSources: sources});
                        }}
                      />
                      <span>CERT-In Feed</span>
                    </label>
                    <label className={`checkbox-pill ${threatSettings.threatIntelSources.includes('dark_web') ? 'active' : ''}`}>
                      <input
                        type="checkbox"
                        checked={threatSettings.threatIntelSources.includes('dark_web')}
                        onChange={(e) => {
                          const sources = e.target.checked
                            ? [...threatSettings.threatIntelSources, 'dark_web']
                            : threatSettings.threatIntelSources.filter(s => s !== 'dark_web');
                          setThreatSettings({...threatSettings, threatIntelSources: sources});
                        }}
                      />
                      <span>Dark Web Monitoring</span>
                    </label>
                  </div>
                </div>

                <div className="form-group" style={{ marginTop: '24px' }}>
                  <label>Analysis Depth</label>
                  <select
                    value={threatSettings.analysisDepth}
                    onChange={(e) => setThreatSettings({...threatSettings, analysisDepth: e.target.value})}
                  >
                    <option value="quick">Quick (API Analysis Only)</option>
                    <option value="standard">Standard (Recommended)</option>
                    <option value="deep">Deep (Full Investigation)</option>
                  </select>
                  <p className="help-text">Higher depth = more detailed analysis but slower processing</p>
                </div>

                <button 
                  type="button" 
                  className="btn-primary"
                  onClick={handleThreatUpdate}
                  disabled={loading}
                  style={{ marginTop: '20px' }}
                >
                  <FiSave /> {loading ? 'Saving...' : 'Save Threat Settings'}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
