<template>
  <div class="product-card">
    <div class="product-image-container">
      <router-link :to="`/products/${product.slug}`">
        <img 
          :src="mainImage" 
          :alt="product.title" 
          class="product-image"
        >
        <span v-if="product.is_new" class="product-badge new">NEW</span>
        <span v-if="salePercentage" class="product-badge sale">-{{ salePercentage }}%</span>
      </router-link>
      <button 
        class="favorite-button"
        :class="{ 'active': isFavorite }"
        @click="toggleFavorite"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="heart-icon">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"></path>
        </svg>
      </button>
    </div>
    
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
import { ref, computed } from 'vue';
import { useStore } from '@/stores/favoriteStore';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const store = useStore();
const isFavorite = computed(() => store.isFavorite(props.product.id));

const mainImage = computed(() => {
  // If there's a main image in the product, use it
  if (props.product.main_image_url) {
    return props.product.main_image_url;
  }
  
  // Fallback to a placeholder if no image is available
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

const toggleFavorite = () => {
  store.toggleFavorite(props.product);
};

const formatPrice = (price) => {
  return `${price} ₽`;
};
</script>

<style scoped>
.product-card {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

.product-image-container {
  position: relative;
  width: 100%;
  padding-top: 133%; /* 3:4 aspect ratio */
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.product-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-image-container:hover .product-image {
  transform: scale(1.05);
}

.product-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 8px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.product-badge.new {
  background-color: #000;
  color: #fff;
}

.product-badge.sale {
  background-color: #ff4b4b;
  color: #fff;
}

.favorite-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.favorite-button:hover {
  background: #fff;
}

.favorite-button.active .heart-icon {
  fill: #ff4b4b;
  stroke: #ff4b4b;
}

.product-info {
  display: flex;
  flex-direction: column;
}

.product-title {
  color: #000;
  text-decoration: none;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  line-height: 1.2;
}

.product-price {
  display: flex;
  gap: 0.5rem;
  align-items: center;
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

@media (min-width: 768px) {
  .product-title {
    font-size: 1rem;
  }
}
</style>