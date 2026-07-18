import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaSignOutAlt, FaUser, FaComments, FaNewspaper } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';
import '../../styles/Layout.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <motion.nav
      className="navbar"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="navbar-container">
        <Link to="/chat" className="navbar-brand">
          <motion.h1 whileHover={{ scale: 1.05 }}>🏦 Banking Assistant</motion.h1>
        </Link>

        <div className="navbar-links">
          <Link to="/chat" className="nav-link">
            <FaComments /> Chat
          </Link>
          <Link to="/updates" className="nav-link">
            <FaNewspaper /> Updates
          </Link>
        </div>

        <div className="navbar-user">
          <span className="user-info">
            <FaUser /> {user?.username}
          </span>
          <motion.button
            className="logout-btn"
            onClick={handleLogout}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FaSignOutAlt /> Logout
          </motion.button>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;
