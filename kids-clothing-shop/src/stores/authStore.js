import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null);
  const token = ref(localStorage.getItem('token') || null);
  const refreshToken = ref(localStorage.getItem('refreshToken') || null);
  const loading = ref(false);

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value);
  const userProfile = computed(() => user.value);

  // Actions
  const login = async (credentials) => {
    loading.value = true;
    try {
      const response = await api.login(credentials);
      
      // Store tokens
      token.value = response.data.access;
      refreshToken.value = response.data.refresh;
      
      localStorage.setItem('token', token.value);
      localStorage.setItem('refreshToken', refreshToken.value);
      
      // Fetch user profile
      await fetchUserProfile();
      
      return response.data;
    } catch (error) {
      // Clear any existing auth data on login failure
      logout();
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const register = async (userData) => {
    loading.value = true;
    try {
      const response = await api.register(userData);
      return response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    user.value = null;
    token.value = null;
    refreshToken.value = null;
    
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  };

  const fetchUserProfile = async () => {
    if (!token.value) return;
    
    try {
      const response = await api.getUserProfile();
      user.value = response.data;
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      // If profile fetch fails, it might mean token is invalid
      if (error.response?.status === 401) {
        logout();
      }
    }
  };

  const refreshAuthToken = async () => {
    if (!refreshToken.value) {
      logout();
      return false;
    }

    try {
      const response = await api.refreshToken(refreshToken.value);
      token.value = response.data.access;
      localStorage.setItem('token', token.value);
      return true;
    } catch (error) {
      console.error('Failed to refresh token:', error);
      logout();
      return false;
    }
  };

  const updateProfile = async (profileData) => {
    loading.value = true;
    try {
      const response = await api.updateUserProfile(profileData);
      user.value = { ...user.value, ...response.data };
      return response.data;
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  // Initialize auth state on store creation
  const initializeAuth = async () => {
    if (token.value) {
      await fetchUserProfile();
    }
  };

  return {
    // State
    user,
    token,
    refreshToken,
    loading,
    
    // Getters
    isAuthenticated,
    userProfile,
    
    // Actions
    login,
    register,
    logout,
    fetchUserProfile,
    refreshAuthToken,
    updateProfile,
    initializeAuth
  };
});