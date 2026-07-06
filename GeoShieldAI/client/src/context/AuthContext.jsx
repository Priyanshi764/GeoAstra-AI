import React, { createContext, useState, useEffect } from 'react';
import api from '../services/api';

export const AuthContext = createContext();

const API_BASE_URL = 'http://127.0.0.1:5000/api';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    // Verify token on mount with timeout
    if (token) {
      verifyToken();
    } else {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Fetch notifications after user is authenticated
    if (isAuthenticated && token) {
      fetchNotifications();
      // Poll for new notifications every 30 seconds
      const pollInterval = setInterval(fetchNotifications, 30000);
      return () => clearInterval(pollInterval);
    }
  }, [isAuthenticated, token]);

  const verifyToken = async () => {
    try {
      // Add timeout to API call
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

      const response = await api.get('/auth/verify-token', {
        headers: { Authorization: `Bearer ${token}` },
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (response.data.success) {
        setUser(response.data.user);
        setIsAuthenticated(true);
      } else {
        logout();
      }
    } catch (error) {
      console.error('Token verification failed:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const fetchNotifications = async () => {
    try {
      const response = await api.get('/user/notifications?limit=10', {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data.success) {
        setNotifications(response.data.notifications || []);
        setUnreadCount(response.data.unread || 0);
      }
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
      // Don't log out, just silently fail
    }
  };

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password });

      if (response.data.success) {
        const newToken = response.data.token;
        setToken(newToken);
        setUser(response.data.user);
        setIsAuthenticated(true);
        localStorage.setItem('token', newToken);
        return { success: true };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (error) {
      return { success: false, message: 'Login failed' };
    }
  };

  const register = async (email, password, name) => {
    try {
      const response = await api.post('/auth/register', { 
        email, 
        password, 
        name,
        role: 'officer'
      });

      if (response.data.success) {
        return { success: true, message: 'Registration successful. Please login.' };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (error) {
      return { success: false, message: 'Registration failed' };
    }
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    setToken(null);
    setNotifications([]);
    setUnreadCount(0);
    localStorage.removeItem('token');
  };

  const markNotificationAsRead = (notificationId) => {
    setNotifications(prev =>
      prev.map(n => n._id === notificationId ? {...n, is_read: true} : n)
    );
    setUnreadCount(Math.max(0, unreadCount - 1));
  };

  const deleteNotification = (notificationId) => {
    setNotifications(prev => prev.filter(n => n._id !== notificationId));
  };

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated,
      loading,
      token,
      login,
      register,
      logout,
      notifications,
      unreadCount,
      markNotificationAsRead,
      deleteNotification,
      fetchNotifications
    }}>
      {children}
    </AuthContext.Provider>
  );
}
