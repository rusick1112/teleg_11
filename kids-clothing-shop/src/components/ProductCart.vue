<template>
  <div class="product-card">
    <div class="product-image-container">
      <router-link :to="`/products/${product.slug}`" class="product-link">
        <!-- Product Image -->
        <div class="product-image-wrapper">
          <img 
            :src="mainImage" 
            :alt="product.title" 
            class="product-image"
          >
        </div>
        
        <!-- Product Badges -->
        <div class="product-badges">
          <span v-if="product.is_new" class="badge badge-new">NEW</span>
          <span v-if="salePercentage" class="badge badge-sale">-{{ salePercentage }}%</span>
        </div>
      </router-link>
      
      <!-- Favorite Button -->
      <button 
        class="favorite-button"
        :class="{ 'active': isFavorite }"
        @click.stop.prevent="toggleFavorite"
        :disabled="isToggling"
        type="button"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          width="20" 
          height="20" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2" 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          class="heart-icon"
        >
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"></path>
        </svg>
      </button>
      
      <!-- Cart Button -->
      <button 
        class="cart-button"
        @click.stop.prevent="addToCart"
        type="button"
        title="Добавить в корзину"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          width="20" 
          height="20" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2" 
          stroke-linecap="round" 
          stroke-linejoin="round"
        >
          <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <path d="M16 10a4 4 0 0 1-8 0"></path>
        </svg>
      </button>
    </div>
    
    <!-- Product Info -->
    <div class="product-info">
      <router-link :to="`/products/${product.slug}`" class="product-title">
        {{ product.title }}
      </router-link>
      
      <div class="product-price">
        <span v-if="product.sale_price" class="sale-price">
          {{ formatPrice(product.sale_price) }}
        </span>
        <span 
          class="regular-price"
          :class="{ 'strike': product.sale_price }"
        >
          {{ formatPrice(product.price) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, nextTick } from 'vue';
import { useFavoriteStore } from '@/stores/favoriteStore';
import { useAuthStore } from '@/stores/authStore';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const favoriteStore = useFavoriteStore();
const authStore = useAuthStore();
const isToggling = ref(false);

// Create a reactive computed that properly tracks the store state
const isFavorite = computed(() => {
  // This forces reactivity by directly checking the store's reactive array
  return favoriteStore.favoriteItems.some(item => item.id === props.product.id);
});

// Debug watcher to see when favorite status changes
watch(isFavorite, (newVal, oldVal) => {
  console.log(`Product ${props.product.id} favorite status: ${oldVal} -> ${newVal}`);
}, { immediate: true });

// Watch for changes in the favorites array
watch(() => favoriteStore.favoriteItems, (newItems) => {
  console.log('Favorites array updated:', newItems.length, 'items');
}, { deep: true });

const mainImage = computed(() => {
  if (props.product.main_image_url) {
    return props.product.main_image_url;
  }
  return '/images/placeholder.jpg';
});

const salePercentage = computed(() => {
  if (props.product.sale_price && props.product.price) {
    const discount = props.product.price - props.product.sale_price;
    const percentage = Math.round((discount / props.product.price) * 100);
    return percentage > 0 ? percentage : null;
  }
  return null;
});

const toggleFavorite = async () => {
  if (isToggling.value) return;
  
  console.log('=== TOGGLE FAVORITE START ===');
  console.log('Product:', props.product.title, 'ID:', props.product.id);
  console.log('Current status:', isFavorite.value);
  console.log('User authenticated:', authStore.isAuthenticated);
  
  isToggling.value = true;
  
  try {
    await favoriteStore.toggleFavorite(props.product);
    
    // Wait for reactivity to update
    await nextTick();
    
    console.log('Toggle completed. New status:', isFavorite.value);
    console.log('Current favorites count:', favoriteStore.favoriteItems.length);
    
  } catch (error) {
    console.error('Toggle favorite error:', error);
  } finally {
    isToggling.value = false;
  }
  
  console.log('=== TOGGLE FAVORITE END ===');
};

const addToCart = () => {
  console.log('Add to cart:', {
    product: props.product.title,
    id: props.product.id
  });
  
  // Add your cart logic here
  // Example: cartStore.addToCart(props.product);
};

const formatPrice = (price) => {
  return `${price} ₽`;
};
</script>

<style scoped>
.product-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.product-image-container {
  position: relative;
  width: 100%;
  aspect-ratio: 3/4;
  overflow: hidden;
  background: #f8f9fa;
  margin-bottom: 0.5rem;
}

.product-link {
  display: block;
  width: 100%;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

.product-image-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.product-badges {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 2;
}

.badge {
  padding: 4px 8px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  border-radius: 2px;
  line-height: 1.2;
}

.badge-new {
  background-color: #000;
  color: #fff;
}

.badge-sale {
  background-color: #ff4b4b;
  color: #fff;
}

.favorite-button,
.cart-button {
  position: absolute;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #6c757d;
  z-index: 10;
}

.favorite-button {
  top: 10px;
  right: 10px;
}

.cart-button {
  top: 10px;
  right: 56px;
}

.favorite-button:hover,
.cart-button:hover {
  background: #fff;
  color: #000;
  transform: scale(1.1);
}

.favorite-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.favorite-button.active {
  background: rgba(255, 75, 75, 0.1);
  color: #ff4b4b;
}

.favorite-button.active .heart-icon {
  fill: #ff4b4b;
  stroke: #ff4b4b;
  animation: heartBeat 0.6s ease-in-out;
}

.heart-icon {
  transition: all 0.3s ease;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.product-info {
  padding: 12px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-title {
  color: #000;
  text-decoration: none;
  font-size: 0.875rem;
  line-height: 1.3;
  font-weight: 500;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.product-title:hover {
  color: #666;
}

.product-price {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-top: auto;
}

.sale-price {
  font-weight: 600;
  color: #ff4b4b;
}

.regular-price {
  color: #000;
}

.strike {
  text-decoration: line-through;
  color: #999;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .product-card {
    border-radius: 6px;
  }
  
  .product-info {
    padding: 10px;
  }
  
  .product-title {
    font-size: 1rem;
  }
  
  .favorite-button,
  .cart-button {
    width: 32px;
    height: 32px;
  }
  
  .cart-button {
    right: 48px;
  }
}
</style>