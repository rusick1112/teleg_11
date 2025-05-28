<template>
      <AppHeader />
  <div class="girls-page">
    <main class="main-content">
      <!-- Girls Hero Carousel -->
      <section class="hero-carousel">
        <Carousel :slides="girlsCarouselSlides" />
      </section>
      
      <!-- New Products Section -->
      <section class="section">
        <div class="container">
          <ProductsGrid 
            title="НОВИНКИ"
            :limit="8"
            view-all-link="/products/new"
            gender="girls"
          />
        </div>
      </section>
      
      <!-- Girls Categories Grid -->
      <section class="section categories-section">
        <div class="container">
          <h2 class="section-title">КАТЕГОРИИ ДЛЯ ДЕВОЧЕК</h2>
          
          <!-- Loading state -->
          <div v-if="loading" class="loading-container">
            <p>Загрузка категорий...</p>
          </div>
          
          <!-- Categories Grid -->
          <div v-else-if="girlsCategories.length > 0" class="categories-grid">
            <router-link 
              v-for="category in girlsCategories" 
              :key="category.id"
              :to="`/categories/girls/${category.slug}`" 
              class="category-card"
            >
              <div class="category-image">
                <img 
                  v-if="category.image" 
                  :src="category.image" 
                  :alt="category.name"
                  class="category-img"
                >
                <div v-else class="image-placeholder" :class="getPlaceholderClass(category.slug)">
                  <div class="placeholder-content">
                    <div class="placeholder-icon">{{ getCategoryIcon(category.slug) }}</div>
                    <p>{{ category.description || 'Коллекция для девочек' }}</p>
                  </div>
                </div>
              </div>
              <div class="category-info">
                <h3 class="category-name">{{ category.name }}</h3>
                <p class="category-count">{{ getCategoryCount(category) }}</p>
              </div>
            </router-link>
          </div>
          
          <!-- No categories message -->
          <div v-else class="no-categories">
            <p>Категории для девочек пока не добавлены</p>
          </div>
        </div>
      </section>
      
      <!-- Featured Collections -->
      <section class="section featured-section">
        <div class="container">
          <h2 class="section-title">ПОПУЛЯРНЫЕ КОЛЛЕКЦИИ</h2>
          <div class="featured-grid">
            <div class="featured-item large">
              <router-link to="/categories/girls/dresses" class="featured-link">
                <div class="featured-image">
                  <div class="image-placeholder dresses-placeholder">
                    <div class="placeholder-content">
                      <div class="placeholder-icon">👗</div>
                      <h3>ПЛАТЬЯ И САРАФАНЫ</h3>
                      <p>Красивые платья для любого случая</p>
                    </div>
                  </div>
                </div>
              </router-link>
            </div>
            
            <div class="featured-item">
              <router-link to="/categories/girls/casual" class="featured-link">
                <div class="featured-image">
                  <div class="image-placeholder casual-placeholder">
                    <div class="placeholder-content">
                      <div class="placeholder-icon">👚</div>
                      <h4>ПОВСЕДНЕВНАЯ ОДЕЖДА</h4>
                    </div>
                  </div>
                </div>
              </router-link>
            </div>
            
            <div class="featured-item">
              <router-link to="/categories/girls/party" class="featured-link">
                <div class="featured-image">
                  <div class="image-placeholder party-placeholder">
                    <div class="placeholder-content">
                      <div class="placeholder-icon">✨</div>
                      <h4>ПРАЗДНИЧНАЯ ОДЕЖДА</h4>
                    </div>
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AppHeader from '@/components/AppHeader.vue';
import Carousel from '@/components/Carousel.vue';
import ProductsGrid from '@/components/ProductsGrid.vue';
import api from '@/services/api';

// Loading state
const loading = ref(true);

// Carousel slides for girls
const girlsCarouselSlides = ref([
  {
    id: 1,
    image: '/images/placeholder-carousel.jpg',
    alt: 'Новая коллекция для девочек',
    title: 'НОВАЯ КОЛЛЕКЦИЯ',
    subtitle: 'Красивая одежда для девочек',
    buttonText: 'СМОТРЕТЬ',
    buttonLink: '/categories/girls/new'
  },
  {
    id: 2,
    image: '/images/placeholder-carousel.jpg',
    alt: 'Праздничные платья',
    title: 'ПРАЗДНИЧНАЯ КОЛЛЕКЦИЯ',
    subtitle: 'Нарядные платья и костюмы',
    buttonText: 'В КАТАЛОГ',
    buttonLink: '/categories/girls/party'
  },
  {
    id: 3,
    image: '/images/placeholder-carousel.jpg',
    alt: 'Школьная форма',
    title: 'ШКОЛЬНАЯ ФОРМА',
    subtitle: 'Стильная и удобная форма',
    buttonText: 'ВЫБРАТЬ',
    buttonLink: '/categories/girls/school'
  }
]);

// Girls categories from API
const girlsCategories = ref([]);

// Icon mapping for categories
const categoryIcons = {
  'platya-i-sarafany': '👗',
  'futbolki-i-majki': '👚',
  'yubki': '🩰',
  'bryuki-i-dzhinsy': '👖',
  'hudi-i-svitshoty': '🧥',
  'bluzki-i-rubashki': '👔',
  'verhnyaya-odezhda': '🧥',
  'obuv': '👠',
  'aksessuary': '👛',
  'nizhnee-bele': '🩲',
  'kostyumy': '👩‍💼'
};

// Placeholder class mapping
const placeholderClasses = {
  'platya-i-sarafany': 'dresses-placeholder',
  'futbolki-i-majki': 'tshirts-placeholder',
  'yubki': 'skirts-placeholder',
  'bryuki-i-dzhinsy': 'pants-placeholder',
  'hudi-i-svitshoty': 'hoodies-placeholder',
  'bluzki-i-rubashki': 'blouses-placeholder',
  'verhnyaya-odezhda': 'outerwear-placeholder',
  'obuv': 'shoes-placeholder',
  'aksessuary': 'accessories-placeholder',
  'nizhnee-bele': 'underwear-placeholder',
  'kostyumy': 'suits-placeholder'
};

// Helper functions
const getCategoryIcon = (slug) => {
  return categoryIcons[slug] || '👚';
};

const getPlaceholderClass = (slug) => {
  return placeholderClasses[slug] || 'default-placeholder';
};

const getCategoryCount = (category) => {
  // You can add product count if your API returns it
  // return category.products_count ? `${category.products_count} товаров` : 'Новая коллекция';
  return 'Новая коллекция';
};

// Fetch girls categories on mount
onMounted(async () => {
  try {
    loading.value = true;
    const response = await api.getGirlsCategories();
    girlsCategories.value = response.data;
    console.log('Girls categories loaded:', girlsCategories.value);
  } catch (error) {
    console.error('Failed to load girls categories:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.main-content {
  padding-top: 120px;
}

/* Loading state */
.loading-container {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.no-categories {
  text-align: center;
  padding: 3rem;
  color: #666;
}

/* Hero Carousel */
.hero-carousel {
  margin-bottom: 2rem;
}

/* Sections */
.section {
  margin: 3rem 0;
  padding: 2rem 0;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #000;
  margin-bottom: 2rem;
  text-align: center;
}

/* Categories Grid */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.category-card {
  text-decoration: none;
  color: inherit;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.category-image {
  width: 100%;
  height: 280px;
  overflow: hidden;
  position: relative;
}

.category-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.category-card:hover .category-img {
  transform: scale(1.05);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: transform 0.3s ease;
}

.category-card:hover .image-placeholder {
  transform: scale(1.05);
}

.placeholder-content {
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
  z-index: 2;
}

.placeholder-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.placeholder-content p {
  font-size: 0.9rem;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Category Placeholders */
.default-placeholder {
  background: linear-gradient(135deg, #9E9E9E, #616161);
}

.tshirts-placeholder {
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
}

.shirts-placeholder {
  background: linear-gradient(135deg, #2196F3, #1565C0);
}

.pants-placeholder {
  background: linear-gradient(135deg, #FF9800, #F57C00);
}

.hoodies-placeholder {
  background: linear-gradient(135deg, #9C27B0, #7B1FA2);
}

.sport-placeholder {
  background: linear-gradient(135deg, #F44336, #D32F2F);
}

.shoes-placeholder {
  background: linear-gradient(135deg, #795548, #5D4037);
}

.accessories-placeholder {
  background: linear-gradient(135deg, #607D8B, #455A64);
}

.underwear-placeholder {
  background: linear-gradient(135deg, #00BCD4, #0097A7);
}

.outerwear-placeholder {
  background: linear-gradient(135deg, #FFC107, #F57F17);
}

.suits-placeholder {
  background: linear-gradient(135deg, #424242, #212121);
}

.category-info {
  padding: 1rem;
  text-align: center;
}

.category-name {
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #000;
  margin: 0 0 0.5rem 0;
  letter-spacing: 0.5px;
}

.category-count {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

/* Featured Collections */
.featured-section {
  background: #f8f9fa;
  border-radius: 20px;
  margin: 4rem 0;
}

.featured-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 2rem;
  height: 400px;
}

.featured-item {
  border-radius: 12px;
  overflow: hidden;
}

.featured-link {
  display: block;
  width: 100%;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

.featured-image {
  width: 100%;
  height: 100%;
  position: relative;
}

.featured-item.large .placeholder-content h3 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.featured-item.large .placeholder-content p {
  font-size: 1.1rem;
}

.featured-item:not(.large) .placeholder-content h4 {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
  text-transform: uppercase;
}

.casual-placeholder {
  background: linear-gradient(135deg, #3F51B5, #303F9F);
}

.formal-placeholder {
  background: linear-gradient(135deg, #212121, #424242);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .featured-grid {
    grid-template-columns: 1fr;
    height: auto;
  }
  
  .featured-item {
    height: 200px;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding-top: 120px;
  }
  
  .categories-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .category-image {
    height: 220px;
  }
  
  .placeholder-icon {
    font-size: 2.5rem;
  }
  
  .featured-item {
    height: 180px;
  }
}

@media (max-width: 480px) {
  .categories-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .container {
    padding: 0 0.5rem;
  }
  
  .section {
    margin: 2rem 0;
    padding: 1rem 0;
  }
}
</style>