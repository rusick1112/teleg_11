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
        
        <button class="action-button" @click="handleUserIconClick">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="user-icon">
            <circle cx="12" cy="8" r="5"/>
            <path d="M20 21a8 8 0 1 0-16 0"/>
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
    
    <div class="menu-overlay" v-if="menuOpen" @click="toggleMenu"></div>
    <div class="side-menu" :class="{ 'open': menuOpen }">
      <div class="side-menu-header">
        <button class="close-button" @click="toggleMenu">×</button>
      </div>
      <nav class="side-nav">
        <router-link to="/categories/girls" class="side-nav-item" @click="toggleMenu">ДЕВОЧКИ</router-link>
        <router-link to="/categories/boys" class="side-nav-item" @click="toggleMenu">МАЛЬЧИКИ</router-link>
        <router-link to="/new-arrivals" class="side-nav-item" @click="toggleMenu">НОВИНКИ</router-link>
        <router-link to="/sale" class="side-nav-item" @click="toggleMenu">РАСПРОДАЖА</router-link>
        <router-link to="/about" class="side-nav-item" @click="toggleMenu">О НАС</router-link>
        <router-link to="/delivery" class="side-nav-item" @click="toggleMenu">ДОСТАВКА</router-link>
      </nav>
    </div>
    
    <!-- Login Modal -->
    <LoginModal :is-open="loginModalOpen" @close="closeLoginModal" />
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import LoginModal from '@/components/LoginModal.vue';

const router = useRouter();
const authStore = useAuthStore();
const menuOpen = ref(false);
const searchOpen = ref(false);
const loginModalOpen = ref(false);
const searchQuery = ref('');
const scrolled = ref(false);
const activeCategory = ref('girls');

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
  if (menuOpen.value && searchOpen.value) {
    searchOpen.value = false;
  }
  
  // Защита от скрола при открытом меню
  if (menuOpen.value) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
};

const toggleSearch = () => {
  searchOpen.value = !searchOpen.value;
  if (searchOpen.value && menuOpen.value) {
    menuOpen.value = false;
    document.body.style.overflow = '';
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

const handleUserIconClick = () => {
  if (authStore.isAuthenticated) {
    // Если аутентифицирован, то переход на страницу профиля
    router.push('/account');
  } else {
    // Форма аутентификации
    loginModalOpen.value = true;
  }
};

const closeLoginModal = () => {
  loginModalOpen.value = false;
};

const handleScroll = () => {
  scrolled.value = window.scrollY > 10;
};

const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    if (menuOpen.value) {
      toggleMenu();
    } else if (searchOpen.value) {
      toggleSearch();
    }
  }
};

onMounted(async () => {
  window.addEventListener('scroll', handleScroll);
  window.addEventListener('keydown', handleKeydown);

  await authStore.initializeAuth();

  const path = router.currentRoute.value.path;
  if (path.includes('/categories/girls')) {
    activeCategory.value = 'girls';
  } else if (path.includes('/categories/boys')) {
    activeCategory.value = 'boys';
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('keydown', handleKeydown);
  document.body.style.overflow = '';
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
.user-icon,
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
  scrollbar-width: none; 
}

.category-nav::-webkit-scrollbar {
  display: none; 
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

.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1001;
  backdrop-filter: blur(3px);
}

.side-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 300px;
  max-width: 80%;
  height: 100%;
  background-color: #fff;
  z-index: 1002;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.side-menu.open {
  transform: translateX(0);
}

.side-menu-header {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.close-button {
  background: none;
  border: none;
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
}

.side-nav {
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
}

.side-nav-item {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  text-decoration: none;
  color: #000;
  font-weight: 500;
  text-transform: uppercase;
  transition: background-color 0.2s ease;
}

.side-nav-item:hover {
  background-color: #f5f5f5;
}

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
  
  .side-menu {
    width: 350px;
  }
}

@media (min-width: 1024px) {
  .category-button {
    padding: 15px 30px;
  }
  
  .side-menu {
    width: 400px;
  }
}
</style>