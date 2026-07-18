import React from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { FaUser, FaRobot, FaExternalLinkAlt } from 'react-icons/fa';
import { format } from 'date-fns';

const ChatMessage = ({ message }) => {
  const isUser = message.type === 'user';

  return (
    <motion.div
      className={`message ${isUser ? 'user-message' : 'bot-message'}`}
      initial={{ opacity: 0, x: isUser ? 20 : -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="message-avatar">
        {isUser ? <FaUser /> : <FaRobot />}
      </div>
      <div className="message-content">
        <div className="message-header">
          <span className="message-sender">{isUser ? 'You' : 'Assistant'}</span>
          <span className="message-time">
            {format(new Date(message.timestamp), 'HH:mm')}
          </span>
        </div>
        <div className="message-text">
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>
        {message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <p className="sources-title">Sources:</p>
            <div className="sources-list">
              {message.sources.slice(0, 3).map((source, index) => (
                <motion.a
                  key={index}
                  href={source.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="source-link"
                  whileHover={{ scale: 1.02 }}
                >
                  <FaExternalLinkAlt size={12} />
                  <span>{source.title}</span>
                </motion.a>
              ))}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ChatMessage;
