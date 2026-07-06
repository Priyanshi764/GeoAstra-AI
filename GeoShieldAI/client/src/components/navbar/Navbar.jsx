import React, { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import { motion, AnimatePresence } from 'framer-motion';
import { FiLogOut, FiMenu, FiX, FiBell, FiClock, FiCheck, FiTrash2 } from 'react-icons/fi';
import axios from 'axios';
import './Navbar.css';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export default function Navbar() {
  const navigate = useNavigate();
  const { user, logout } = useContext(AuthContext);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loadingNotifications, setLoadingNotifications] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    fetchNotifications();
    // Poll for notifications every 30 seconds
    const pollTimer = setInterval(fetchNotifications, 30000);
    return () => clearInterval(pollTimer);
  }, []);

  const fetchNotifications = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE_URL}/user/notifications?limit=10`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data.success) {
        setNotifications(response.data.notifications || []);
        setUnreadCount(response.data.unread || 0);
      }
    } catch (err) {
      console.error('Failed to fetch notifications:', err);
      // Use demo notifications for demo mode
      setNotifications(getDemoNotifications());
      setUnreadCount(3);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        `${API_BASE_URL}/user/notifications/${notificationId}/read`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );

      // Update local state
      setNotifications(prev =>
        prev.map(n => n._id === notificationId ? {...n, is_read: true} : n)
      );
      setUnreadCount(Math.max(0, unreadCount - 1));
    } catch (err) {
      console.error('Failed to mark notification as read:', err);
    }
  };

  const deleteNotification = (notificationId) => {
    setNotifications(prev => prev.filter(n => n._id !== notificationId));
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const formattedTime = currentTime.toLocaleTimeString('en-US', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });

  const getDemoNotifications = () => [
    {
      _id: '1',
      type: 'threat',
      title: 'Critical Threat Detected',
      message: 'High-risk malware detected targeting SBI banking system',
      created_at: new Date(Date.now() - 300000).toISOString(),
      is_read: false,
      severity: 'critical'
    },
    {
      _id: '2',
      type: 'threat',
      title: 'Phishing Campaign',
      message: 'New phishing emails detected in Bhopal district',
      created_at: new Date(Date.now() - 900000).toISOString(),
      is_read: false,
      severity: 'high'
    },
    {
      _id: '3',
      type: 'incident',
      title: 'Incident Created',
      message: 'Automatic incident ticket created for ransomware threat',
      created_at: new Date(Date.now() - 1800000).toISOString(),
      is_read: false,
      severity: 'high'
    }
  ];

  const getNotificationIcon = (type, severity) => {
    if (type === 'threat' && severity === 'critical') return '🔴';
    if (type === 'threat' && severity === 'high') return '🟠';
    if (type === 'threat') return '🟡';
    if (type === 'incident') return '⚠️';
    if (type === 'system') return 'ℹ️';
    return '📢';
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-left">
          <div className="navbar-logo">
            <div className="logo-icon">🛡️</div>
            <span>GeoAstra AI</span>
          </div>
        </div>

        <div className="navbar-center">
          <div className="live-clock">
            <FiClock size={16} />
            <span>{formattedTime}</span>
          </div>
        </div>

        <div className="navbar-right">
          {/* Notification Bell */}
          <div className="notification-wrapper">
            <button 
              className="icon-button notification-button" 
              title="Notifications"
              onClick={() => setIsNotificationOpen(!isNotificationOpen)}
            >
              <FiBell size={20} />
              {unreadCount > 0 && (
                <span className="notification-badge">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              )}
            </button>

            {/* Notification Panel */}
            <AnimatePresence>
              {isNotificationOpen && (
                <motion.div
                  className="notification-panel"
                  initial={{ opacity: 0, y: -10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -10, scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="notification-header">
                    <h3>Notifications</h3>
                    {unreadCount > 0 && (
                      <span className="unread-badge">{unreadCount} new</span>
                    )}
                  </div>

                  <div className="notification-list">
                    {notifications.length > 0 ? (
                      notifications.map((notif) => (
                        <motion.div
                          key={notif._id}
                          className={`notification-item ${notif.is_read ? 'read' : 'unread'} ${notif.severity || 'info'}`}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: 20 }}
                        >
                          <div className="notification-icon">
                            {getNotificationIcon(notif.type, notif.severity)}
                          </div>

                          <div className="notification-content">
                            <div className="notification-title">{notif.title}</div>
                            <div className="notification-message">{notif.message}</div>
                            <div className="notification-time">{formatTime(notif.created_at)}</div>
                          </div>

                          <div className="notification-actions">
                            {!notif.is_read && (
                              <button
                                className="action-btn check"
                                onClick={() => markAsRead(notif._id)}
                                title="Mark as read"
                              >
                                <FiCheck size={16} />
                              </button>
                            )}
                            <button
                              className="action-btn delete"
                              onClick={() => deleteNotification(notif._id)}
                              title="Delete"
                            >
                              <FiTrash2 size={16} />
                            </button>
                          </div>
                        </motion.div>
                      ))
                    ) : (
                      <div className="no-notifications">
                        <p>No notifications</p>
                      </div>
                    )}
                  </div>

                  <div className="notification-footer">
                    <button 
                      className="view-all-btn"
                      onClick={() => {
                        navigate('/settings');
                        setIsNotificationOpen(false);
                      }}
                    >
                      View All Notifications →
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <motion.div
            className="user-menu"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="user-avatar">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <span className="user-name">{user?.name || 'Officer'}</span>
            <span className="user-role">{user?.role}</span>
          </motion.div>

          <button
            className="logout-button"
            onClick={handleLogout}
            title="Logout"
          >
            <FiLogOut size={20} />
          </button>

          <button
            className="menu-toggle"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>
        </div>
      </div>

      {/* Overlay for notification panel */}
      <AnimatePresence>
        {isNotificationOpen && (
          <motion.div
            className="notification-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsNotificationOpen(false)}
          />
        )}
      </AnimatePresence>
    </nav>
  );
}
