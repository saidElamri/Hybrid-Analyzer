/**
 * Token management utilities for JWT authentication.
 */

const TOKEN_KEY = 'hybrid_analyzer_token';
const USER_KEY = 'hybrid_analyzer_user';

export const tokenManager = {
  /**
   * Save JWT token to localStorage
   */
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  /**
   * Get JWT token from localStorage
   */
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  /**
   * Remove JWT token from localStorage
   */
  removeToken() {
    localStorage.removeItem(TOKEN_KEY);
  },

  /**
   * Save user data to localStorage
   */
  setUser(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  /**
   * Get user data from localStorage
   */
  getUser() {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  },

  /**
   * Remove user data from localStorage
   */
  removeUser() {
    localStorage.removeItem(USER_KEY);
  },

  /**
   * Clear all authentication data
   */
  clearAuth() {
    this.removeToken();
    this.removeUser();
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!this.getToken();
  }
};
