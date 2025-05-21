<template>
  <header class="header" :class="{ 'scrolled': scrolled }">
    <div class="header-content">
      <button class="menu-button" @click="toggleMenu">
        <span class="menu-icon"></span>
      </button>
      
      <router-link to="/" class="logo">
        <img src="@/assets/logo.svg" alt="kids" />
      </router-link>
      
      <div class="header-actions">
        <button class="action-button" @click="toggleSearch">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="search-icon">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>
        
        <router-link to="/favorites" class="action-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="heart-icon">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"></path>
          </svg>
        </router-link>
        
        <router-link to="/cart" class="action-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="cart-icon">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <path d="M16 10a4 4 0 0 1-8 0"></path>
          </svg>
        </router-link>
      </div>
    </div>
    
    <nav class="category-nav">
      <router-link 
        to="/categories/girls" 
        class="category-button"
        :class="{ 'active': activeCategory === 'girls' }"
        @click="setActiveCategory('girls')"
      >
        ДЕВОЧКИ
      </router-link>
      <router-link 
        to="/categories/boys" 
        class="category-button"
        :class="{ 'active': activeCategory === 'boys' }"
        @click="setActiveCategory('boys')"
      >
        МАЛЬЧИКИ
      </router-link>
    </nav>
    
    <div class="search-panel" v-if="searchOpen">
      <div class="search-container">
        <input 
          type="text" 
          placeholder="Поиск..." 
          v-model="searchQuery"
          @keyup.enter="performSearch"
        >
        <button @click="performSearch" class="search-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>
      </div>
    </div>
    
    <div class="mobile-menu" v-if="menuOpen">
      <div class="mobile-menu-header">
        <button class="close-button" @click="toggleMenu">×</button>
      </div>
      <nav class="mobile-nav">
        <router-link to="/categories/girls" class="mobile-nav-item">ДЕВОЧКИ</router-link>
        <router-link to="/categories/boys" class="mobile-nav-item">МАЛЬЧИКИ</router-link>
        <router-link to="/new-arrivals" class="mobile-nav-item">НОВИНКИ</router-link>
        <router-link to="/sale" class="mobile-nav-item">РАСПРОДАЖА</router-link>
        <router-link to="/about" class="mobile-nav-item">О НАС</router-link>
        <router-link to="/delivery" class="mobile-nav-item">ДОСТАВКА</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const menuOpen = ref(false);
const searchOpen = ref(false);
const searchQuery = ref('');
const scrolled = ref(false);
const activeCategory = ref('girls'); // Default to girls category

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
  // Close search if it's open
  if (menuOpen.value && searchOpen.value) {
    searchOpen.value = false;
  }
};

const toggleSearch = () => {
  searchOpen.value = !searchOpen.value;
  // Close menu if it's open
  if (searchOpen.value && menuOpen.value) {
    menuOpen.value = false;
  }
};

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value } });
    searchOpen.value = false;
    searchQuery.value = '';
  }
};

const setActiveCategory = (category) => {
  activeCategory.value = category;
};

const handleScroll = () => {
  scrolled.value = window.scrollY > 10;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  // Set active category based on current route
  const path = router.currentRoute.value.path;
  if (path.includes('/categories/girls')) {
    activeCategory.value = 'girls';
  } else if (path.includes('/categories/boys')) {
    activeCategory.value = 'boys';
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #ffffff;
  z-index: 1000;
  transition: box-shadow 0.3s ease;
}

.header.scrolled {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  height: 60px;
}

.logo {
  height: 30px;
}

.logo img {
  height: 100%;
  width: auto;
}

.menu-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-icon {
  display: block;
  position: relative;
  width: 24px;
  height: 2px;
  background-color: #000;
}

.menu-icon::before,
.menu-icon::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background-color: #000;
  left: 0;
  transition: transform 0.3s ease;
}

.menu-icon::before {
  top: -6px;
}

.menu-icon::after {
  bottom: -6px;
}

.header-actions {
  display: flex;
  gap: 16px;
}

.action-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
}

.search-icon,
.heart-icon,
.cart-icon {
  width: 24px;
  height: 24px;
}

.category-nav {
  display: flex;
  border-top: 1px solid #e0e0e0;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none; /* Firefox */
}

.category-nav::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.category-button {
  flex: 1;
  padding: 12px 20px;
  text-align: center;
  color: #000;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.3s ease;
  white-space: nowrap;
  text-transform: uppercase;
  font-size: 0.875rem;
}

.category-button.active {
  background-color: #000;
  color: #fff;
}

.search-panel {
  position: absolute;
  top: 60px;
  left: 0;
  width: 100%;
  background-color: #fff;
  padding: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.search-container {
  display: flex;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.search-container input {
  flex: 1;
  padding: 10px 16px;
  border: none;
  outline: none;
  font-size: 1rem;
}

.search-btn {
  background-color: #000;
  color: #fff;
  border: none;
  padding: 0 16px;
  cursor: pointer;
}

.mobile-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #fff;
  z-index: 1001;
  overflow-y: auto;
}

.mobile-menu-header {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.mobile-nav-item {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  text-decoration: none;
  color: #000;
  font-weight: 500;
  text-transform: uppercase;
}

/* Responsive adjustments */
@media (min-width: 768px) {
  .header-content {
    padding: 1rem 2rem;
  }
  
  .category-nav {
    padding: 0 2rem;
  }
  
  .category-button {
    font-size: 1rem;
  }
}

@media (min-width: 1024px) {
  .menu-button {
    display: none;
  }
  
  .mobile-menu {
    display: none;
  }
  
  .category-button {
    padding: 15px 30px;
  }
}
</style>