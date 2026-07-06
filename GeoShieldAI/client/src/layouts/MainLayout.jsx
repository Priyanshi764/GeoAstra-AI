import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from '../components/navbar/Navbar';
import Sidebar from '../components/sidebar/Sidebar';
import './MainLayout.css';

export default function MainLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  return (
    <div className="main-layout">
      <Navbar />
      <div className="layout-container">
        <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
        <main className={`main-content ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
          <div className="content-wrapper">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
