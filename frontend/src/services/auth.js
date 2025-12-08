/**
 * Authentication service for login and registration.
 */
import api from './api';
import { tokenManager } from '../utils/tokenManager';

export const authService = {
  /**
   * Register a new user
   */
  async register(username, email, password) {
    const response = await api.post('/auth/register', {
      username,
      email,
      password,
    });

    const { access_token, user } = response.data;
    
    // Save token and user data
    tokenManager.setToken(access_token);
    tokenManager.setUser(user);

    return response.data;
  },

  /**
   * Login existing user
   */
  async login(username, password) {
    const response = await api.post('/auth/login', {
      username,
      password,
    });

    const { access_token, user } = response.data;
    
    // Save token and user data
    tokenManager.setToken(access_token);
    tokenManager.setUser(user);

    return response.data;
  },

  /**
   * Logout user
   */
  logout() {
    tokenManager.clearAuth();
  },

  /**
   * Get current user
   */
  getCurrentUser() {
    return tokenManager.getUser();
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return tokenManager.isAuthenticated();
  },
};
