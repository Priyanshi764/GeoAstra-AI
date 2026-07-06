import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  FiHome,
  FiUpload,
  FiMap,
  FiRss,
  FiBarChart2,
  FiInbox,
  FiFileText,
  FiCpu,
  FiSettings,
  FiChevronRight,
  FiShield,
  FiAlertTriangle
} from 'react-icons/fi';
import './Sidebar.css';

export default function Sidebar({ isOpen, setIsOpen }) {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: FiHome },
    { path: '/upload', label: 'Upload Intelligence', icon: FiUpload },
    { path: '/cyber-zones', label: 'Cyber Zones', icon: FiShield },
    { path: '/geofence-alerts', label: 'Geofence Alerts', icon: FiAlertTriangle },
    { path: '/heatmap', label: 'Cyber Geofence Map', icon: FiMap },
    { path: '/live-feed', label: 'Live Feed', icon: FiRss },
    { path: '/analytics', label: 'Analytics', icon: FiBarChart2 },
    { path: '/investigation', label: 'Investigation', icon: FiInbox },
    { path: '/assistant', label: 'AI Assistant', icon: FiCpu },
    { path: '/settings', label: 'Settings', icon: FiSettings },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <>
      <motion.div
        className={`sidebar ${isOpen ? 'open' : 'closed'}`}
        initial={{ x: -280 }}
        animate={{ x: isOpen ? 0 : -280 }}
        transition={{ duration: 0.3 }}
      >
        <div className="sidebar-header">
          <h3>Menu</h3>
          <button
            className="close-btn"
            onClick={() => setIsOpen(false)}
          >
            ×
          </button>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);

            return (
              <motion.button
                key={item.path}
                className={`nav-item ${active ? 'active' : ''}`}
                onClick={() => {
                  navigate(item.path);
                  if (window.innerWidth < 1024) {
                    setIsOpen(false);
                  }
                }}
                whileHover={{ x: 5 }}
                whileTap={{ scale: 0.98 }}
              >
                <Icon size={20} className="nav-icon" />
                <span className="nav-label">{item.label}</span>
                {active && <FiChevronRight size={18} className="nav-indicator" />}
              </motion.button>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="status-item">
            <div className="status-dot active"></div>
            <span>System Online</span>
          </div>
          <div className="status-item">
            <div className="status-dot connected"></div>
            <span>Database Connected</span>
          </div>
        </div>
      </motion.div>

      {isOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
