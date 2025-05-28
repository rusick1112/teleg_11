import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/services/api';

export const useFavoriteStore = defineStore('favorite', () => {
  const favoriteItems = ref([]);
  const loading = ref(false);

  // Initialize from localStorage for non-authenticated users
  const initializeFromLocalStorage = () => {
    const savedFavorites = localStorage.getItem('favorites');
    if (savedFavorites) {
      try {
        const parsed = JSON.parse(savedFavorites);
        favoriteItems.value = Array.isArray(parsed) ? parsed : [];
        console.log('Loaded favorites from localStorage:', favoriteItems.value);
      } catch (error) {
        console.error('Error parsing favorites from localStorage:', error);
        favoriteItems.value = [];
      }
    }
  };

  // Save to localStorage
  const saveToLocalStorage = () => {
    try {
      localStorage.setItem('favorites', JSON.stringify(favoriteItems.value));
      console.log('Saved favorites to localStorage:', favoriteItems.value.length, 'items');
    } catch (error) {
      console.error('Error saving favorites to localStorage:', error);
    }
  };

  // Check if product is in favorites
  const isFavorite = (productId) => {
    const result = favoriteItems.value.some(item => item.id === productId);
    console.log(`Checking if product ${productId} is favorite:`, result);
    return result;
  };

  // Add product to favorites (internal method)
  const addToFavorites = (product) => {
    const exists = favoriteItems.value.some(item => item.id === product.id);
    if (!exists) {
      favoriteItems.value.push(product);
      saveToLocalStorage();
      console.log('Added product to favorites:', product.title);
      return true;
    }
    return false;
  };

  // Remove product from favorites (internal method)
  const removeFromFavorites = (productId) => {
    const index = favoriteItems.value.findIndex(item => item.id === productId);
    if (index > -1) {
      const removed = favoriteItems.value.splice(index, 1)[0];
      saveToLocalStorage();
      console.log('Removed product from favorites:', removed.title);
      return true;
    }
    return false;
  };

  // Toggle favorite status
  const toggleFavorite = async (product) => {
    console.log('=== STORE TOGGLE FAVORITE START ===');
    console.log('Product:', product);
    
    // Handle case where only ID is passed
    let productId;
    let productData;
    
    if (typeof product === 'number' || typeof product === 'string') {
      productId = parseInt(product);
      productData = null;
    } else {
      productId = product.id;
      productData = product;
    }
    
    console.log('Product ID:', productId);
    console.log('Current favorites:', favoriteItems.value.map(f => f.id));
    
    const wasInFavorites = isFavorite(productId);
    console.log('Was in favorites:', wasInFavorites);
    
    // Import auth store dynamically to avoid circular dependency
    const { useAuthStore } = await import('@/stores/authStore');
    const authStore = useAuthStore();
    
    // If user is authenticated, sync with API first
    if (authStore.isAuthenticated) {
      try {
        console.log('User authenticated, calling API...');
        const response = await api.toggleFavorite(productId);
        console.log('API response:', response.data);
        
        // Update local state based on API response
        if (response.data.status === 'добавлен') {
          if (productData) {
            addToFavorites(productData);
          }
          console.log('Product added via API');
        } else if (response.data.status === 'удалён') {
          removeFromFavorites(productId);
          console.log('Product removed via API');
        }
        
      } catch (error) {
        console.error('API error, falling back to local storage:', error);
        
        // Fallback to local storage behavior
        if (wasInFavorites) {
          removeFromFavorites(productId);
        } else if (productData) {
          addToFavorites(productData);
        }
      }
    } else {
      // For non-authenticated users, just update local state
      console.log('User not authenticated, using local storage only');
      if (wasInFavorites) {
        removeFromFavorites(productId);
      } else if (productData) {
        addToFavorites(productData);
      }
    }
    
    console.log('Final favorites:', favoriteItems.value.map(f => f.id));
    console.log('=== STORE TOGGLE FAVORITE END ===');
  };

  // Public add to favorites
  const addFavorite = (product) => {
    addToFavorites(product);
  };

  // Public remove from favorites
  const removeFavorite = (productId) => {
    removeFromFavorites(productId);
  };

  // Clear all favorites
  const clearFavorites = () => {
    favoriteItems.value = [];
    saveToLocalStorage();
    console.log('Cleared all favorites');
  };

  // Sync favorites with API data
  const syncFavorites = (apiProducts) => {
    favoriteItems.value = Array.isArray(apiProducts) ? apiProducts : [];
    saveToLocalStorage();
    console.log('Synced favorites with API:', favoriteItems.value.length, 'items');
  };

  // Load favorites from API for authenticated users
  const loadFavoritesFromAPI = async () => {
    if (loading.value) return; // Prevent multiple simultaneous loads
    
    loading.value = true;
    try {
      console.log('Loading favorites from API...');
      const response = await api.getFavorites();
      const apiFavorites = response.data.results || response.data;
      console.log('Raw API favorites response:', apiFavorites);
      
      // Extract products from the API response
      const products = apiFavorites.map(fav => fav.product || fav);
      favoriteItems.value = products;
      saveToLocalStorage();
      
      console.log('Successfully loaded', products.length, 'favorites from API');
    } catch (error) {
      console.error('Error loading favorites from API:', error);
      // Don't clear local favorites on error
    } finally {
      loading.value = false;
    }
  };

  // Computed properties
  const favoriteCount = computed(() => favoriteItems.value.length);
  const hasFavorites = computed(() => favoriteItems.value.length > 0);

  // Initialize store
  initializeFromLocalStorage();

  return {
    favoriteItems,
    loading,
    favoriteCount,
    hasFavorites,
    
    isFavorite,
    toggleFavorite,
    addFavorite,
    removeFavorite,
    clearFavorites,
    syncFavorites,
    loadFavoritesFromAPI
  };
});