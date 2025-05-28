<template>
  <div class="favorites-page">
    <AppHeader />
    <div class="container">
      <div class="favorites-header">
        <h1>Избранное</h1>
        <p class="favorites-count" v-if="favorites.length > 0">
          {{ favorites.length }} {{ getProductWord(favorites.length) }}
        </p>
      </div>
      
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Загрузка избранных товаров...</p>
      </div>
      
      <div v-else-if="error" class="error-container">
        <p>{{ error }}</p>
        <button @click="fetchFavorites" class="retry-button">
          Попробовать снова
        </button>
      </div>
      
      <div v-else-if="favorites.length === 0" class="empty-favorites">
        <div class="empty-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"></path>
          </svg>
        </div>
        <h2>В избранном пока пусто</h2>
        <p>Добавляйте товары в избранное, чтобы вернуться к ним позже</p>
        <router-link to="/" class="continue-shopping-button">
          Продолжить покупки
        </router-link>
      </div>
      
      <div v-else class="favorites-grid">
        <div 
          v-for="favorite in favorites" 
          :key="favorite.id || `local-${favorite.product?.id}`"
          class="favorite-item"
        >
          <ProductCard :product="getProductFromFavorite(favorite)" />
          <button 
            @click="removeFavorite(getProductFromFavorite(favorite).id)" 
            class="remove-button"
            :disabled="removingId === getProductFromFavorite(favorite).id"
          >
            {{ removingId === getProductFromFavorite(favorite).id ? 'Удаляется...' : 'Удалить из избранного' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AppHeader from '@/components/AppHeader.vue';
import { useAuthStore } from '@/stores/authStore';
import { useFavoriteStore } from '@/stores/favoriteStore';
import ProductCard from '@/components/ProductCart.vue'; // Note: Using your existing component name
import api from '@/services/api';

const authStore = useAuthStore();
const favoriteStore = useFavoriteStore();

const favorites = ref([]);
const loading = ref(false);
const error = ref('');
const removingId = ref(null);

const getProductWord = (count) => {
  const lastDigit = count % 10;
  const lastTwoDigits = count % 100;
  
  if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
    return 'товаров';
  }
  
  if (lastDigit === 1) {
    return 'товар';
  }
  
  if (lastDigit >= 2 && lastDigit <= 4) {
    return 'товара';
  }
  
  return 'товаров';
};

const getProductFromFavorite = (favorite) => {
  // Handle both API format (with .product) and local format (direct product)
  return favorite.product || favorite;
};

const fetchFavorites = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    if (authStore.isAuthenticated) {
      // Fetch favorites from API for authenticated users
      console.log('Fetching favorites from API for authenticated user');
      const response = await api.getFavorites();
      console.log('API favorites response:', response.data);
      favorites.value = response.data.results || response.data;
      
      // Sync with local store
      favoriteStore.syncFavorites(favorites.value.map(f => f.product));
    } else {
      // Use local favorites for non-authenticated users
      console.log('Using local favorites for non-authenticated user');
      favorites.value = favoriteStore.favoriteItems.map(product => ({
        id: `local-${product.id}`,
        product: product
      }));
      console.log('Local favorites:', favorites.value);
    }
  } catch (err) {
    console.error('Error fetching favorites:', err);
    error.value = 'Ошибка загрузки избранных товаров. Попробуйте еще раз.';
    
    // Fallback to local favorites
    favorites.value = favoriteStore.favoriteItems.map(product => ({
      id: `local-${product.id}`,
      product: product
    }));
  } finally {
    loading.value = false;
  }
};

const removeFavorite = async (productId) => {
  removingId.value = productId;
  
  try {
    if (authStore.isAuthenticated) {
      // Remove from API
      await api.toggleFavorite(productId);
    }
    
    // Remove from local store
    favoriteStore.removeFavorite(productId);
    
    // Remove from local list
    favorites.value = favorites.value.filter(f => {
      const product = getProductFromFavorite(f);
      return product.id !== productId;
    });
  } catch (err) {
    console.error('Error removing favorite:', err);
    error.value = 'Ошибка при удалении товара из избранного';
  } finally {
    removingId.value = null;
  }
};

onMounted(() => {
  fetchFavorites();
});
</script>

<style scoped>
.favorites-page {
  padding-top: 120px;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.favorites-header {
  margin-bottom: 2rem;
}

.favorites-header h1 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.favorites-count {
  color: #666;
  font-size: 1rem;
}

.loading-container,
.error-container {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  color: #ff4b4b;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s ease;
}

.retry-button:hover {
  opacity: 0.9;
}

.empty-favorites {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  margin-bottom: 2rem;
  color: #e0e0e0;
}

.empty-favorites h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.empty-favorites p {
  color: #666;
  margin-bottom: 2rem;
}

.continue-shopping-button {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: #000;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: opacity 0.2s ease;
}

.continue-shopping-button:hover {
  opacity: 0.9;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}

.favorite-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.favorite-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.remove-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #f5f5f5;
  border: none;
  color: #666;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.remove-button:hover {
  background-color: #ff4b4b;
  color: white;
}

.remove-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Responsive design */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
  
  .favorites-header h1 {
    font-size: 1.5rem;
  }
  
  .favorites-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 1rem;
  }
  
  .empty-favorites {
    padding: 3rem 1.5rem;
  }
}

@media (min-width: 992px) {
  .favorites-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1200px) {
  .favorites-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}
</style>