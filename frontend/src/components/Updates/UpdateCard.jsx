import React from 'react';
import { motion } from 'framer-motion';
import { FaExternalLinkAlt, FaNewspaper } from 'react-icons/fa';

const UpdateCard = ({ update, index }) => {
  const getCategoryColor = (category) => {
    const colors = {
      loans: '#4CAF50',
      rbi: '#2196F3',
      farmers: '#FF9800',
      insurance: '#9C27B0',
      general: '#607D8B',
    };
    return colors[category] || colors.general;
  };

  return (
    <motion.div
      className="update-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ scale: 1.02, boxShadow: '0 8px 16px rgba(0,0,0,0.2)' }}
    >
      <div
        className="update-category-badge"
        style={{ backgroundColor: getCategoryColor(update.category) }}
      >
        {update.category}
      </div>

      <div className="update-content">
        <div className="update-icon">
          <FaNewspaper size={24} />
        </div>
        <h3 className="update-title">{update.title}</h3>
        <p className="update-description">{update.description}</p>

        {update.url && (
          <motion.a
            href={update.url}
            target="_blank"
            rel="noopener noreferrer"
            className="update-link"
            whileHover={{ scale: 1.05 }}
          >
            <FaExternalLinkAlt /> Read More
          </motion.a>
        )}
      </div>
    </motion.div>
  );
};

export default UpdateCard;
