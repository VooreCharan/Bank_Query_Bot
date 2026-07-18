import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaPaperPlane, FaTrash, FaMapMarkerAlt } from 'react-icons/fa';
import { toast } from 'react-toastify';
import { chatAPI } from '../../services/api';
import ChatMessage from './ChatMessage';
import VoiceInput from './VoiceInput';
import BankSelector from './BankSelector';
import LocationSearch from './LocationSearch';
import '../../styles/Chat.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [selectedBank, setSelectedBank] = useState('');
  const [language, setLanguage] = useState('en');
  const [showLocationSearch, setShowLocationSearch] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    initializeSession();
  }, [selectedBank]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const initializeSession = async () => {
    try {
      const response = await chatAPI.newSession({ bank_name: selectedBank });
      setSessionId(response.data.session.session_id);
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const handleSendMessage = async (message = inputMessage) => {
    if (!message.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage({
        message,
        session_id: sessionId,
        bank_name: selectedBank,
        language,
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.response,
        sources: response.data.sources,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);

      // Check if response needs location search
      if (response.data.needs_location) {
        setTimeout(() => {
          setShowLocationSearch(true);
        }, 500);
      }
    } catch (error) {
      toast.error('Failed to send message');
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleVoiceInput = (transcript) => {
    setInputMessage(transcript);
  };

  const handleLocationSelect = (bank) => {
    const locationMessage = `📍 **${bank.name}** (${bank.type})\n\n` +
      `**Address:** ${bank.address}\n` +
      `**Distance:** ${bank.distance_km} km away\n` +
      (bank.phone ? `**Phone:** ${bank.phone}\n` : '') +
      (bank.opening_hours ? `**Hours:** ${bank.opening_hours}\n` : '') +
      `\n[View on Google Maps](https://www.google.com/maps/search/?api=1&query=${bank.lat},${bank.lon})`;

    const botMessage = {
      id: Date.now(),
      type: 'bot',
      content: locationMessage,
      sources: [],
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, botMessage]);
    setShowLocationSearch(false);
    toast.success('Location added to chat');
  };

  const clearChat = () => {
    setMessages([]);
    initializeSession();
    toast.info('Chat cleared');
  };

  const quickQuestions = [
    'How to check bank balance?',
    'How to open a savings account?',
    'Find bank branches near me',
    'How to apply for a personal loan?',
    'Reset internet banking password',
  ];

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <BankSelector
          selectedBank={selectedBank}
          onBankSelect={setSelectedBank}
        />
        <div className="chat-actions">
          <motion.button
            className="location-btn"
            onClick={() => setShowLocationSearch(true)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            title="Find nearby banks and ATMs"
          >
            <FaMapMarkerAlt /> Find Locations
          </motion.button>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="language-selector"
          >
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="te">తెలుగు</option>
            <option value="ta">தமிழ்</option>
            <option value="bn">বাংলা</option>
            <option value="mr">मराठी</option>
          </select>
          <motion.button
            className="clear-chat-btn"
            onClick={clearChat}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FaTrash /> Clear
          </motion.button>
        </div>
      </div>

      <div className="chat-messages">
        <AnimatePresence>
          {messages.length === 0 && (
            <motion.div
              className="welcome-message"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
            >
              <h2>Welcome to Banking Assistant</h2>
              <p>How can I help you today?</p>
              <div className="quick-questions">
                {quickQuestions.map((question, index) => (
                  <motion.button
                    key={index}
                    className="quick-question-btn"
                    onClick={() => handleSendMessage(question)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    {question}
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}

          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div
            className="typing-indicator"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <span></span>
            <span></span>
            <span></span>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message or use voice input..."
            className="chat-input"
            rows="1"
          />
          <div className="input-actions">
            <VoiceInput onTranscript={handleVoiceInput} language={language} />
            <motion.button
              className="send-button"
              onClick={() => handleSendMessage()}
              disabled={loading || !inputMessage.trim()}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FaPaperPlane />
            </motion.button>
          </div>
        </div>
      </div>

      {/* Location Search Modal */}
      <AnimatePresence>
        {showLocationSearch && (
          <LocationSearch
            onClose={() => setShowLocationSearch(false)}
            onLocationSelect={handleLocationSelect}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default ChatInterface;
