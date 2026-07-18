import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data) => api.put('/auth/profile', data),
};

export const chatAPI = {
  sendMessage: (data) => api.post('/chat', data),
  newSession: (data) => api.post('/chat/new-session', data),
  getSessions: () => api.get('/chat/sessions'),
  getBanks: () => api.get('/banks'),
  searchLocations: (data) => api.post('/search-locations', data),
};

export const updatesAPI = {
  getUpdates: (params) => api.get('/updates', { params }),
  getCategories: () => api.get('/updates/categories'),
};

export default api;
