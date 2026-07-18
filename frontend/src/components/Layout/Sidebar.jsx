import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FaHome,
  FaComments,
  FaNewspaper,
  FaHistory,
  FaCog,
  FaQuestionCircle,
  FaBars,
  FaTimes,
  FaChartLine,
  FaUser,
} from 'react-icons/fa';
import '../../styles/Sidebar.css';

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', icon: FaHome, label: 'Dashboard' },
    { path: '/chat', icon: FaComments, label: 'Chat' },
    { path: '/updates', icon: FaNewspaper, label: 'Latest Updates' },
    { path: '/history', icon: FaHistory, label: 'Chat History' },
    { path: '/analytics', icon: FaChartLine, label: 'Analytics' },
    { path: '/faq', icon: FaQuestionCircle, label: 'FAQs' },
    { path: '/profile', icon: FaUser, label: 'Profile' },
    { path: '/settings', icon: FaCog, label: 'Settings' },
  ];

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const sidebarVariants = {
    open: {
      x: 0,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 30,
      },
    },
    closed: {
      x: '-100%',
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 30,
      },
    },
  };

  return (
    <>
      {/* Mobile Toggle Button */}
      <motion.button
        className="sidebar-toggle"
        onClick={toggleSidebar}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        {isOpen ? <FaTimes /> : <FaBars />}
      </motion.button>

      {/* Overlay for mobile */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="sidebar-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={toggleSidebar}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        className={`sidebar ${isOpen ? 'open' : ''}`}
        variants={sidebarVariants}
        initial="closed"
        animate={isOpen ? 'open' : 'closed'}
      >
        <div className="sidebar-header">
          <motion.h2
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            🏦 Banking Assistant
          </motion.h2>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item, index) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <motion.div
                key={item.path}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Link
                  to={item.path}
                  className={`sidebar-link ${isActive ? 'active' : ''}`}
                  onClick={() => setIsOpen(false)}
                >
                  <motion.div
                    className="sidebar-link-content"
                    whileHover={{ x: 5 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Icon className="sidebar-icon" />
                    <span className="sidebar-label">{item.label}</span>
                  </motion.div>
                  {isActive && (
                    <motion.div
                      className="active-indicator"
                      layoutId="activeIndicator"
                      initial={false}
                      transition={{
                        type: 'spring',
                        stiffness: 300,
                        damping: 30,
                      }}
                    />
                  )}
                </Link>
              </motion.div>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            © 2025 Banking Chatbot
          </motion.p>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;
