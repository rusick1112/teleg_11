<template>
  <div class="products-grid-section">
    <div class="section-header">
      <h2 class="section-title">{{ title }}</h2>
      <router-link v-if="viewAllLink" :to="viewAllLink" class="view-all">
        смотреть все <span class="arrow">→</span>
      </router-link>
    </div>
    
    <div v-if="loading" class="loading-container">
      <p>Загрузка товаров...</p>
    </div>
    
    <div v-else-if="products.length > 0" class="product-grid">
      <ProductCard 
        v-for="product in products" 
        :key="product.id" 
        :product="product" 
      />
    </div>
    
    <div v-else class="no-products">
      <p>Товары не найдены</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ProductCard from '@/components/ProductCart.vue';
import api from '@/services/api';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  limit: {
    type: Number,
    default: 8
  },
  viewAllLink: {
    type: String,
    default: null
  },
  gender: {
    type: String,
    default: null, // 'boys', 'girls', or null for all
    validator: (value) => ['boys', 'girls', null].includes(value)
  }
});

const loading = ref(true);
const products = ref([]);

onMounted(async () => {
  try {
    loading.value = true;
    let response;
    
    // Fetch products based on gender prop
    if (props.gender === 'boys') {
      response = await api.getBoysProducts({ limit: props.limit });
    } else if (props.gender === 'girls') {
      response = await api.getGirlsProducts({ limit: props.limit });
    } else {
      response = await api.getProducts({ limit: props.limit });
    }
    
    products.value = response.data.results || response.data;
    console.log(`${props.gender || 'All'} products loaded:`, products.value);
  } catch (error) {
    console.error('Failed to load products:', error);
    products.value = [];
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.products-grid-section {
  width: 100%;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  text-transform: uppercase;
  margin: 0;
}

.view-all {
  color: #000;
  font-size: 0.9rem;
  text-decoration: none;
  display: flex;
  align-items: center;
  transition: opacity 0.2s;
}

.view-all:hover {
  opacity: 0.7;
}

.arrow {
  margin-left: 4px;
}

.loading-container {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.no-products {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 1rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
}
</style>