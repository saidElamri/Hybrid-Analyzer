/**
 * Custom hook for authentication state management.
 */
import { useState, useEffect } from 'react';
import { authService } from '../services/auth';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication status on mount
    const currentUser = authService.getCurrentUser();
    const authenticated = authService.isAuthenticated();

    setUser(currentUser);
    setIsAuthenticated(authenticated);
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    const data = await authService.login(username, password);
    setUser(data.user);
    setIsAuthenticated(true);
    return data;
  };

  const register = async (username, email, password) => {
    const data = await authService.register(username, email, password);
    setUser(data.user);
    setIsAuthenticated(true);
    return data;
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  return {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
  };
};
