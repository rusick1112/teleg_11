<template>
  <div class="product-card">
    <div class="product-image-container">
      <router-link :to="`/products/${product.slug}`" class="product-link">
        <!-- Product Image -->
        <div class="product-image-wrapper">
          <img 
            v-if="mainImage" 
            :src="mainImage" 
            :alt="product.title" 
            class="product-image"
            @error="handleImageError"
          >
          <div v-else class="product-image-placeholder">
            <div class="placeholder-icon">👕</div>
          </div>
        </div>
        
        <!-- Product Badges -->
        <div class="product-badges">
          <span v-if="isNew" class="badge badge-new">NEW</span>
          <span v-if="salePercentage" class="badge badge-sale">-{{ salePercentage }}%</span>
        </div>
      </router-link>
      
      <!-- Favorite Button -->
      <button 
        class="favorite-button"
        :class="{ 'active': isFavorite }"
        @click="toggleFavorite"
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
        >
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"></path>
        </svg>
      </button>
      
      <!-- Cart Button -->
      <button 
        class="cart-button"
        @click="addToCart"
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
    
    <!-- Color Options -->
    <div class="color-options" v-if="availableColors.length > 1">
      <button 
        v-for="color in availableColors.slice(0, 4)" 
        :key="color.id"
        class="color-dot"
        :style="{ backgroundColor: color.code }"
        :title="color.name"
        @click="selectColor(color)"
      ></button>
      <span v-if="availableColors.length > 4" class="color-more">
        +{{ availableColors.length - 4 }}
      </span>
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
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
// import { useFavoriteStore } from '@/stores/favoriteStore';
// import { useCartStore } from '@/stores/cartStore';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const authStore = useAuthStore();
// const favoriteStore = useFavoriteStore();
// const cartStore = useCartStore();

const imageError = ref(false);
const selectedColorId = ref(null);

// Computed properties
const mainImage = computed(() => {
  if (imageError.value) return null;
  
  // Get the selected variant or default variant
  const variant = selectedVariant.value;
  if (variant && variant.images && variant.images.length > 0) {
    // Return the first image (sorted by sort_order)
    const sortedImages = variant.images.sort((a, b) => a.sort_order - b.sort_order);
    return sortedImages[0].image;
  }
  
  return null;
});

const selectedVariant = computed(() => {
  if (!props.product.variants || props.product.variants.length === 0) {
    return null;
  }
  
  if (selectedColorId.value) {
    return props.product.variants.find(v => v.color.id === selectedColorId.value);
  }
  
  // Return default variant or first variant
  return props.product.variants.find(v => v.is_default) || props.product.variants[0];
});

const availableColors = computed(() => {
  if (!props.product.variants) return [];
  return props.product.variants.map(variant => variant.color);
});

const isNew = computed(() => {
  if (!props.product.created_at) return false;
  const createdDate = new Date(props.product.created_at);
  const now = new Date();
  const daysDiff = (now - createdDate) / (1000 * 60 * 60 * 24);
  return daysDiff <= 30; // Consider new if created within 30 days
});

const salePercentage = computed(() => {
  if (props.product.sale_price && props.product.price) {
    const discount = props.product.price - props.product.sale_price;
    const percentage = Math.round((discount / props.product.price) * 100);
    return percentage > 0 ? percentage : null;
  }
  return null;
});

const isFavorite = computed(() => {
  // This would connect to your favorite store
  // return favoriteStore.isFavorite(props.product.id);
  return false;
});

// Methods
const handleImageError = () => {
  imageError.value = true;
};

const selectColor = (color) => {
  selectedColorId.value = color.id;
};

const toggleFavorite = () => {
  if (!authStore.isAuthenticated) {
    // Show login modal or redirect
    console.log('Please login to add favorites');
    return;
  }
  
  // favoriteStore.toggleFavorite(props.product);
  console.log('Toggle favorite for product:', props.product.id);
};

const addToCart = () => {
  const variant = selectedVariant.value;
  if (!variant) {
    console.log('No variant selected');
    return;
  }
  
  // For now, just add the first available size
  const availableStock = variant.stocks?.find(stock => stock.quantity > 0);
  if (!availableStock) {
    console.log('Product out of stock');
    return;
  }
  
  // cartStore.addToCart({
  //   product_stock_id: availableStock.id,
  //   quantity: 1
  // });
  
  console.log('Add to cart:', {
    product: props.product.title,
    variant: variant.color.name,
    size: availableStock.size.name
  });
};

const formatPrice = (price) => {
  return `${Math.round(price)} ₽`;
};

onMounted(() => {
  // Set default selected color if available
  if (availableColors.value.length > 0) {
    const defaultVariant = props.product.variants?.find(v => v.is_default);
    if (defaultVariant) {
      selectedColorId.value = defaultVariant.color.id;
    }
  }
});
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

.product-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  color: #6c757d;
}

.placeholder-icon {
  font-size: 3rem;
  opacity: 0.5;
}

.product-badges {
  position: absolute;
  top: 8px;
  left: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 2;
}

.badge {
  padding: 2px 6px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  border-radius: 2px;
  line-height: 1.2;
}

.badge-new {
  background-color: #000;
  color: #fff;
}

.badge-sale {
  background-color: #dc3545;
  color: #fff;
}

.favorite-button,
.cart-button {
  position: absolute;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6c757d;
  z-index: 3;
}

.favorite-button {
  top: 8px;
  right: 8px;
}

.cart-button {
  top: 8px;
  right: 48px;
}

.favorite-button:hover,
.cart-button:hover {
  background: #fff;
  color: #000;
  transform: scale(1.1);
}

.favorite-button.active {
  color: #dc3545;
  background: #fff;
}

.favorite-button.active svg {
  fill: currentColor;
}

.color-options {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: #fff;
}

.color-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 0 0 1px #e9ecef;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.color-dot:hover {
  transform: scale(1.2);
}

.color-more {
  font-size: 0.75rem;
  color: #6c757d;
  margin-left: 4px;
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
  font-size: 0.9rem;
  line-height: 1.3;
  font-weight: 500;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-title:hover {
  color: #007bff;
}

.product-price {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: auto;
}

.sale-price {
  font-weight: 700;
  color: #dc3545;
  font-size: 1rem;
}

.regular-price {
  font-weight: 600;
  color: #000;
  font-size: 1rem;
}

.regular-price.strike {
  text-decoration: line-through;
  color: #6c757d;
  font-weight: 400;
  font-size: 0.9rem;
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
    font-size: 0.85rem;
  }
  
  .sale-price,
  .regular-price {
    font-size: 0.9rem;
  }
  
  .favorite-button,
  .cart-button {
    width: 28px;
    height: 28px;
  }
  
  .cart-button {
    right: 42px;
  }
}
</style>