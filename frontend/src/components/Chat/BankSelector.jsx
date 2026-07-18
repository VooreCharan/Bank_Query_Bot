import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaUniversity } from 'react-icons/fa';
import { chatAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const BankSelector = ({ selectedBank, onBankSelect }) => {
  const [banks, setBanks] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const { updateUser } = useAuth();

  useEffect(() => {
    fetchBanks();
  }, []);

  const fetchBanks = async () => {
    try {
      const response = await chatAPI.getBanks();
      setBanks(response.data.banks);
    } catch (error) {
      console.error('Error fetching banks:', error);
    }
  };

  const handleBankSelect = async (bank) => {
    onBankSelect(bank);
    setIsOpen(false);
    await updateUser({ selected_bank: bank });
  };

  return (
    <div className="bank-selector">
      <motion.button
        className="bank-selector-btn"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.02 }}
      >
        <FaUniversity />
        <span>{selectedBank || 'Select Bank'}</span>
      </motion.button>

      {isOpen && (
        <motion.div
          className="bank-dropdown"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
        >
          <div className="bank-list">
            <button
              className="bank-option"
              onClick={() => handleBankSelect('')}
            >
              All Banks (General)
            </button>
            {banks.map((bank, index) => (
              <button
                key={index}
                className="bank-option"
                onClick={() => handleBankSelect(bank)}
              >
                {bank}
              </button>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default BankSelector;
