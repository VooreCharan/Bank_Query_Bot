/**
 * Application-wide constants
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
};

// Authentication
export const AUTH_CONFIG = {
  TOKEN_KEY: 'auth_token',
  USER_KEY: 'user_data',
  TOKEN_EXPIRY_DAYS: 1,
  REFRESH_THRESHOLD_MINUTES: 5,
};

// Supported Languages
export const LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
  { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം' },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ' },
];

// Indian Banks
export const INDIAN_BANKS = [
  'State Bank of India (SBI)',
  'HDFC Bank',
  'ICICI Bank',
  'Axis Bank',
  'Punjab National Bank (PNB)',
  'Bank of Baroda',
  'Canara Bank',
  'Union Bank of India',
  'Bank of India',
  'IndusInd Bank',
  'Kotak Mahindra Bank',
  'Yes Bank',
  'IDBI Bank',
  'Central Bank of India',
  'Indian Bank',
  'UCO Bank',
  'Bank of Maharashtra',
  'Indian Overseas Bank',
  'Punjab & Sind Bank',
  'Federal Bank',
];

// Update Categories
export const UPDATE_CATEGORIES = [
  { id: 'all', name: 'All Updates', color: '#607D8B' },
  { id: 'loans', name: 'Loan Updates', color: '#4CAF50' },
  { id: 'rbi', name: 'RBI Updates', color: '#2196F3' },
  { id: 'farmers', name: 'Farmer Schemes', color: '#FF9800' },
  { id: 'insurance', name: 'Insurance Updates', color: '#9C27B0' },
  { id: 'general', name: 'General Banking', color: '#607D8B' },
];

// Quick Questions
export const QUICK_QUESTIONS = [
  'How to check bank balance?',
  'How to open a savings account?',
  'Find bank branches near me',
  'How to apply for a personal loan?',
  'Reset internet banking password',
  'How to link Aadhaar with bank account?',
  'What are the documents required for account opening?',
  'How to activate mobile banking?',
  'How to request a new debit card?',
  'What is the minimum balance requirement?',
];

// FAQ Categories
export const FAQ_CATEGORIES = [
  'Account Management',
  'Loans & Credit',
  'Cards & Payments',
  'Digital Banking',
  'KYC & Documentation',
  'Transactions',
  'Security & Fraud',
  'General Queries',
];

// Chat Message Types
export const MESSAGE_TYPES = {
  USER: 'user',
  BOT: 'bot',
  SYSTEM: 'system',
  ERROR: 'error',
};

// Animation Variants
export const ANIMATION_VARIANTS = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
  },
  slideUp: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 },
  },
  slideLeft: {
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: 20 },
  },
  scale: {
    initial: { opacity: 0, scale: 0.9 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.9 },
  },
};

// Theme Colors
export const THEME_COLORS = {
  primary: '#1e88e5',
  secondary: '#26a69a',
  accent: '#ff6b6b',
  success: '#4CAF50',
  warning: '#FF9800',
  error: '#f44336',
  info: '#2196F3',
  dark: '#1a1a2e',
  light: '#f5f5f5',
};

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PER_PAGE: 10,
  MAX_PER_PAGE: 100,
};

// Date Formats
export const DATE_FORMATS = {
  FULL: 'MMMM dd, yyyy HH:mm:ss',
  DATE_ONLY: 'MMMM dd, yyyy',
  TIME_ONLY: 'HH:mm:ss',
  SHORT: 'MM/dd/yyyy',
  ISO: "yyyy-MM-dd'T'HH:mm:ss",
};

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_DATA: 'user_data',
  THEME: 'theme_preference',
  LANGUAGE: 'language_preference',
  SELECTED_BANK: 'selected_bank',
  CHAT_HISTORY: 'chat_history',
  PREFERENCES: 'user_preferences',
};

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  SERVER_ERROR: 'Server error. Please try again later.',
  AUTHENTICATION_ERROR: 'Authentication failed. Please login again.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  UNKNOWN_ERROR: 'An unexpected error occurred.',
  SESSION_EXPIRED: 'Your session has expired. Please login again.',
};

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'Login successful!',
  REGISTER_SUCCESS: 'Registration successful! Please login.',
  UPDATE_SUCCESS: 'Updated successfully!',
  DELETE_SUCCESS: 'Deleted successfully!',
  SAVE_SUCCESS: 'Saved successfully!',
};

// Regex Patterns
export const REGEX_PATTERNS = {
  EMAIL: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
  PHONE: /^[6-9]\d{9}$/,
  PINCODE: /^[1-9][0-9]{5}$/,
  PAN: /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/,
  AADHAAR: /^\d{12}$/,
  IFSC: /^[A-Z]{4}0[A-Z0-9]{6}$/,
};

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
};

// Voice Recognition Config
export const VOICE_CONFIG = {
  CONTINUOUS: false,
  INTERIM_RESULTS: false,
  MAX_ALTERNATIVES: 1,
  LANGUAGE_MAP: {
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
  },
};

// Export default object with all constants
export default {
  API_CONFIG,
  AUTH_CONFIG,
  LANGUAGES,
  INDIAN_BANKS,
  UPDATE_CATEGORIES,
  QUICK_QUESTIONS,
  FAQ_CATEGORIES,
  MESSAGE_TYPES,
  ANIMATION_VARIANTS,
  THEME_COLORS,
  PAGINATION,
  DATE_FORMATS,
  STORAGE_KEYS,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  REGEX_PATTERNS,
  HTTP_STATUS,
  VOICE_CONFIG,
};
