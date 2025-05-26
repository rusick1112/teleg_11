<template>
    <AppHeader />
  <div class="account-page">
    <div class="container">
      <div class="account-header">
        <h1>Личный кабинет</h1>
        <button @click="handleLogout" class="logout-button">
          Выйти
        </button>
      </div>
      
      <div class="account-content" v-if="authStore.userProfile">
        <div class="account-section">
          <div class="section-header">
            <h2>Информация о профиле</h2>
          </div>
          <div class="profile-info">
            <div class="info-row">
              <span class="info-label">Логин:</span>
              <span class="info-value">{{ getUserData('username') }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Email:</span>
              <span class="info-value">{{ getUserData('email') }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">ФИО:</span>
              <span class="info-value">{{ getUserData('first_name') }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Телефон:</span>
              <span class="info-value">{{ authStore.userProfile.phone_number || 'Не указан' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Адрес:</span>
              <span class="info-value">{{ authStore.userProfile.address || 'Не указан' }}</span>
            </div>
          </div>
        </div>
        
        <div class="account-section">
          <h2>Быстрые действия</h2>
          <div class="quick-actions">
            <router-link to="/orders" class="action-card">
              <div class="action-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                  <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                </svg>
              </div>
              <div class="action-content">
                <h3>Мои заказы</h3>
                <p>Просмотр истории заказов</p>
              </div>
            </router-link>
            
            <router-link to="/favorites" class="action-card">
              <div class="action-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
              </div>
              <div class="action-content">
                <h3>Избранное</h3>
                <p>Сохраненные товары</p>
              </div>
            </router-link>
            
            <button @click="openEditModal" class="action-card action-button-card">
              <div class="action-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 6L9 17l-5-5"></path>
                </svg>
              </div>
              <div class="action-content">
                <h3>Редактировать профиль</h3>
                <p>Изменить личные данные</p>
              </div>
            </button>
          </div>
        </div>
      </div>
      
      <div v-else-if="authStore.loading" class="loading">
        Загрузка профиля...
      </div>
      
      <div v-else class="error">
        Ошибка загрузки профиля
      </div>
    </div>
    
    <!-- Модальное окно для изменения профиля -->
    <EditProfileModal 
      :is-open="editModalOpen" 
      @close="closeEditModal"
      @updated="handleProfileUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AppHeader from '@/components/AppHeader.vue';
import { useAuthStore } from '@/stores/authStore';
import EditProfileModal from '@/components/EditProfileModal.vue';

const router = useRouter();
const authStore = useAuthStore();
const editModalOpen = ref(false);

const getUserData = (field) => {
  const profile = authStore.userProfile;
  if (!profile) return 'Не указано';

  if (profile.user && profile.user[field]) {
    return profile.user[field];
  }

  if (profile[field]) {
    return profile[field];
  }
  
  return 'Не указано';
};

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};

const openEditModal = () => {
  editModalOpen.value = true;
};

const closeEditModal = () => {
  editModalOpen.value = false;
};

const handleProfileUpdated = async () => {
  await authStore.fetchUserProfile();
};

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/');
    return;
  }

  if (!authStore.userProfile) {
    await authStore.fetchUserProfile();
  }
});
</script>

<style scoped>
.account-page {
  padding-top: 120px;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.account-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.logout-button {
  background-color: #ff4b4b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.logout-button:hover {
  background-color: #e63c3c;
}

.account-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.account-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.account-section h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.edit-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #000;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: opacity 0.2s ease;
}

.edit-button:hover {
  opacity: 0.9;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.info-label {
  font-weight: 500;
  color: #555;
  font-size: 0.875rem;
}

.info-value {
  color: #333;
  font-size: 1rem;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
  background: white;
}

.action-button-card {
  cursor: pointer;
  border: none;
  background: white;
  border: 1px solid #e0e0e0;
  text-align: left;
}

.action-card:hover {
  border-color: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background-color: #f5f5f5;
  border-radius: 8px;
  color: #666;
  flex-shrink: 0;
}

.action-content h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: #333;
}

.action-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.account-section h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.profile-info p {
  margin: 0;
  color: #666;
}

.profile-info strong {
  color: #333;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.action-card {
  display: block;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
}

.action-card:hover {
  border-color: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.action-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #333;
}

.action-card p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error {
  color: #ff4b4b;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
  
  .account-header {
    padding: 2rem;
  }
  
  .account-section {
    padding: 2rem;
  }
}

@media (max-width: 768px) {
  .account-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
}
</style>