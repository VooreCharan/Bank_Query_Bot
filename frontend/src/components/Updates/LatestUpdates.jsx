import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaSync } from 'react-icons/fa';
import { updatesAPI } from '../../services/api';
import UpdateCard from './UpdateCard';
import '../../styles/Updates.css';

const LatestUpdates = () => {
  const [updates, setUpdates] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCategories();
    fetchUpdates();
  }, []);

  useEffect(() => {
    fetchUpdates();
  }, [selectedCategory]);

  const fetchCategories = async () => {
    try {
      const response = await updatesAPI.getCategories();
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchUpdates = async () => {
    setLoading(true);
    try {
      const response = await updatesAPI.getUpdates({
        category: selectedCategory,
        limit: 20,
      });
      setUpdates(response.data.updates);
    } catch (error) {
      console.error('Error fetching updates:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="updates-container">
      <div className="updates-header">
        <h1>Latest Banking Updates</h1>
        <motion.button
          className="refresh-btn"
          onClick={fetchUpdates}
          whileHover={{ scale: 1.05}}
          whileTap={{ scale: 0.95 }}
        >
          <FaSync /> Refresh
        </motion.button>
      </div>

      <div className="category-filters">
        {categories.map((category) => (
          <motion.button
            key={category.id}
            className={`category-btn ${
              selectedCategory === category.id ? 'active' : ''
            }`}
            onClick={() => setSelectedCategory(category.id)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {category.name}
          </motion.button>
        ))}
      </div>

      <div className="updates-grid">
        {loading ? (
          <div className="loading-spinner">Loading updates...</div>
        ) : updates.length > 0 ? (
          updates.map((update, index) => (
            <UpdateCard key={index} update={update} index={index} />
          ))
        ) : (
          <div className="no-updates">No updates available</div>
        )}
      </div>
    </div>
  );
};

export default LatestUpdates;
