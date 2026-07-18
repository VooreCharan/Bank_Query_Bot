import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaMicrophone, FaMicrophoneSlash } from 'react-icons/fa';
import SpeechRecognition, {
  useSpeechRecognition,
} from 'react-speech-recognition';
import { toast } from 'react-toastify';

const VoiceInput = ({ onTranscript, language = 'en' }) => {
  const [isListening, setIsListening] = useState(false);
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  useEffect(() => {
    if (transcript && !listening) {
      onTranscript(transcript);
      resetTranscript();
    }
  }, [transcript, listening]);

  const handleVoiceInput = () => {
    if (!browserSupportsSpeechRecognition) {
      toast.error('Browser does not support speech recognition');
      return;
    }

    if (isListening) {
      SpeechRecognition.stopListening();
      setIsListening(false);
    } else {
      resetTranscript();
      SpeechRecognition.startListening({
        continuous: false,
        language: getLanguageCode(language),
      });
      setIsListening(true);
    }
  };

  const getLanguageCode = (lang) => {
    const languageCodes = {
      en: 'en-US',
      hi: 'hi-IN',
      te: 'te-IN',
      ta: 'ta-IN',
      bn: 'bn-IN',
      mr: 'mr-IN',
      gu: 'gu-IN',
      kn: 'kn-IN',
      ml: 'ml-IN',
      pa: 'pa-IN',
    };
    return languageCodes[lang] || 'en-US';
  };

  return (
    <motion.button
      className={`voice-input-btn ${isListening ? 'listening' : ''}`}
      onClick={handleVoiceInput}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      animate={isListening ? { scale: [1, 1.1, 1] } : {}}
      transition={isListening ? { repeat: Infinity, duration: 1 } : {}}
    >
      {isListening ? <FaMicrophone /> : <FaMicrophoneSlash />}
    </motion.button>
  );
};

export default VoiceInput;
