<template>
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
          <h2>Информация о профиле</h2>
          <div class="profile-info">
            <p><strong>Имя пользователя:</strong> {{ getUserData('username') }}</p>
            <p><strong>Email:</strong> {{ getUserData('email') }}</p>
            <p><strong>ФИО:</strong> {{ getUserData('first_name') }}</p>
            <p><strong>Телефон:</strong> {{ authStore.userProfile.phone_number || 'Не указан' }}</p>
            <p><strong>Адрес:</strong> {{ authStore.userProfile.address || 'Не указан' }}</p>
          </div>
        </div>
        
        <div class="account-section">
          <h2>Быстрые действия</h2>
          <div class="quick-actions">
            <router-link to="/orders" class="action-card">
              <h3>Мои заказы</h3>
              <p>Просмотр истории заказов</p>
            </router-link>
            
            <router-link to="/favorites" class="action-card">
              <h3>Избранное</h3>
              <p>Сохраненные товары</p>
            </router-link>
            
            <router-link to="/profile/edit" class="action-card">
              <h3>Редактировать профиль</h3>
              <p>Изменить личные данные</p>
            </router-link>
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
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const authStore = useAuthStore();

const getUserData = (field) => {
  const profile = authStore.userProfile;
  if (!profile) return 'Не указано';
  
  // Try to get from user object first, then from profile directly
  if (profile.user && profile.user[field]) {
    return profile.user[field];
  }
  
  // If no user object, try to get from profile directly
  if (profile[field]) {
    return profile[field];
  }
  
  return 'Не указано';
};

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};

onMounted(async () => {
  // Redirect to home if not authenticated
  if (!authStore.isAuthenticated) {
    router.push('/');
    return;
  }
  
  // Fetch user profile if not already loaded
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