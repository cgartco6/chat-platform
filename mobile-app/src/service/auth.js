import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { api } from './api';

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = await AsyncStorage.getItem('authToken');
      const userData = await AsyncStorage.getItem('userData');
      
      if (token && userData) {
        setUser(JSON.parse(userData));
        // Set the token for API requests
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await api.post('/api/login', { email, password });
      
      if (response.data.access_token) {
        const { access_token, user_id, username } = response.data;
        
        // Store token and user data
        await AsyncStorage.setItem('authToken', access_token);
        await AsyncStorage.setItem('userData', JSON.stringify({
          id: user_id,
          username: username
        }));
        
        // Set the token for API requests
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        setUser({ id: user_id, username: username });
        return { success: true };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await api.post('/api/register', userData);
      
      if (response.data.access_token) {
        const { access_token, user_id, username } = response.data;
        
        // Store token and user data
        await AsyncStorage.setItem('authToken', access_token);
        await AsyncStorage.setItem('userData', JSON.stringify({
          id: user_id,
          username: username
        }));
        
        // Set the token for API requests
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        setUser({ id: user_id, username: username });
        return { success: true };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { 
        success: false, 
        error: error.response?.data?.error || 'Registration failed' 
      };
    }
  };

  const logout = async () => {
    try {
      await AsyncStorage.removeItem('authToken');
      await AsyncStorage.removeItem('userData');
      setUser(null);
      delete api.defaults.headers.common['Authorization'];
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
