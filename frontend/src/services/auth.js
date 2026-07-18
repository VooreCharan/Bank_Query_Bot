import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Authentication service for managing user authentication
 */
class AuthService {
  constructor() {
    this.tokenKey = 'auth_token';
    this.userKey = 'user_data';
  }

  /**
   * Login user and store token
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<Object>} User data and token
   */
  async login(email, password) {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        email,
        password,
      });

      const { access_token, user } = response.data;

      // Store token and user data
      this.setToken(access_token);
      this.setUser(user);

      return { success: true, user, token: access_token };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Login failed',
      };
    }
  }

  /**
   * Register new user
   * @param {string} username - Username
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise<Object>} Registration result
   */
  async register(username, email, password) {
    try {
      const response = await axios.post(`${API_URL}/auth/register`, {
        username,
        email,
        password,
      });

      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Registration failed',
      };
    }
  }

  /**
   * Logout user and clear stored data
   */
  logout() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    sessionStorage.clear();
  }

  /**
   * Get current user profile
   * @returns {Promise<Object>} User profile data
   */
  async getProfile() {
    try {
      const token = this.getToken();
      
      if (!token) {
        throw new Error('No token found');
      }

      const response = await axios.get(`${API_URL}/auth/profile`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const user = response.data.user;
      this.setUser(user);

      return { success: true, user };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to fetch profile',
      };
    }
  }

  /**
   * Update user profile
   * @param {Object} data - Profile data to update
   * @returns {Promise<Object>} Updated user data
   */
  async updateProfile(data) {
    try {
      const token = this.getToken();

      const response = await axios.put(`${API_URL}/auth/profile`, data, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const user = response.data.user;
      this.setUser(user);

      return { success: true, user };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to update profile',
      };
    }
  }

  /**
   * Store authentication token
   * @param {string} token - JWT token
   */
  setToken(token) {
    localStorage.setItem(this.tokenKey, token);
  }

  /**
   * Get stored authentication token
   * @returns {string|null} JWT token or null
   */
  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  /**
   * Store user data
   * @param {Object} user - User data object
   */
  setUser(user) {
    localStorage.setItem(this.userKey, JSON.stringify(user));
  }

  /**
   * Get stored user data
   * @returns {Object|null} User data or null
   */
  getUser() {
    const userData = localStorage.getItem(this.userKey);
    return userData ? JSON.parse(userData) : null;
  }

  /**
   * Check if user is authenticated
   * @returns {boolean} Authentication status
   */
  isAuthenticated() {
    const token = this.getToken();
    
    if (!token) {
      return false;
    }

    // Check if token is expired (basic check)
    try {
      const payload = this.decodeToken(token);
      const currentTime = Date.now() / 1000;
      
      return payload.exp > currentTime;
    } catch (error) {
      return false;
    }
  }

  /**
   * Decode JWT token (without verification)
   * @param {string} token - JWT token
   * @returns {Object} Decoded token payload
   */
  decodeToken(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      return JSON.parse(jsonPayload);
    } catch (error) {
      throw new Error('Invalid token');
    }
  }

  /**
   * Refresh authentication token
   * @returns {Promise<Object>} New token
   */
  async refreshToken() {
    try {
      const token = this.getToken();

      const response = await axios.post(
        `${API_URL}/auth/refresh`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const newToken = response.data.access_token;
      this.setToken(newToken);

      return { success: true, token: newToken };
    } catch (error) {
      this.logout();
      return {
        success: false,
        error: 'Token refresh failed',
      };
    }
  }

  /**
   * Change user password
   * @param {string} currentPassword - Current password
   * @param {string} newPassword - New password
   * @returns {Promise<Object>} Result
   */
  async changePassword(currentPassword, newPassword) {
    try {
      const token = this.getToken();

      const response = await axios.post(
        `${API_URL}/auth/change-password`,
        {
          current_password: currentPassword,
          new_password: newPassword,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      return { success: true, message: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Password change failed',
      };
    }
  }
}

// Create singleton instance
const authService = new AuthService();

export default authService;
