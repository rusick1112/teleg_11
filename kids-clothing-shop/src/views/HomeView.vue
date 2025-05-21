<!-- src/views/HomeView.vue -->
<template>
  <div class="home">
    
     <main class="main-content"> 
      <!-- Carousel -->
      <section class="carousel-section">
        <Carousel :slides="heroSlides" />
      </section>
      
      <!-- Новые товары -->
      <!-- <section class="section">
        <div class="section-header">
          <h2 class="section-title">НОВИНКИ</h2>
          <router-link to="/products/new" class="view-all">
            смотреть все <span class="arrow">→</span>
          </router-link>
        </div>
        
        <div class="product-grid">
          <ProductCard 
            v-for="product in newProducts" 
            :key="product.id" 
            :product="product" 
          />
        </div>
      </section> -->
      
      <!-- Categories Banner -->
      <!-- <section class="categories-banner">
        <div class="category">
          <img src="@/assets/outerwear-boys.jpg" alt="Верхняя одежда мальчики">
          <div class="category-content">
            <h3>ВЕРХНЯЯ<br>одежда</h3>
            <router-link to="/categories/outerwear/boys" class="category-btn">
              НОВИНКИ
            </router-link>
            <div class="category-tabs">
              <router-link to="/categories/outerwear/girls" class="tab">
                ДЕВОЧКИ
              </router-link>
              <router-link to="/categories/outerwear/boys" class="tab active">
                МАЛЬЧИКИ
              </router-link>
            </div>
          </div>
        </div>
      </section> -->
    </main> 
    

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Carousel from '@/components/Carousel.vue';
// import ProductCard from '@/components/ProductCard.vue';
import api from '@/services/api';

// Состояние слайдера
// const newProducts = ref([]);
const heroSlides = ref([
  { id: 1, image: '/images/imageFront.webp', alt: 'New Collection' },
  { id: 2, image: '/images/imageFront.webp', alt: 'Summer Collection' }
]);


// Fetch новых товаров
// onMounted(async () => {
//   try {
//     const response = await api.getProducts({ category: 'new', limit: 6 });
//     newProducts.value = response.data;
//   } catch (error) {
//     console.error('Failed to fetch new products:', error);
//   }
  

// });
</script>

<style scoped>
.main-content {
  padding-top: 120px; /* Adjust based on header height */
}

.section {
  margin: 2rem 1rem;
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
}

.view-all {
  color: #000;
  font-size: 0.9rem;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.arrow {
  margin-left: 4px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
}

.categories-banner {
  margin: 2rem 0;
}

.category {
  position: relative;
  height: 70vh;
  overflow: hidden;
}

.category img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-content {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 2rem;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.category-content h3 {
  font-size: 2.5rem;
  font-weight: 700;
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 1.5rem;
}

.category-btn {
  background-color: #00b8d4;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 500;
  text-transform: uppercase;
  text-decoration: none;
  margin-bottom: 1.5rem;
}

.category-tabs {
  display: flex;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 30px;
  overflow: hidden;
  margin-top: 1rem;
}

.tab {
  padding: 0.75rem 1.5rem;
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
}

.tab.active {
  background: black;
  border-radius: 30px;
}

/* Responsive adjustments */
@media (min-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
  
  .section {
    margin: 3rem 2rem;
  }
}

@media (min-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(6, 1fr);
  }
  
  .section {
    margin: 4rem;
  }
}
</style>