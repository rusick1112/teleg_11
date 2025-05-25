<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">Вход или регистрация</h2>
        <button class="close-button" @click="closeModal">×</button>
      </div>
      
      <div class="modal-body">
        <div class="auth-tabs">
          <button 
            class="auth-tab"
            :class="{ 'active': activeTab === 'login' }"
            @click="activeTab = 'login'"
          >
            Войти в аккаунт
          </button>
          <button 
            class="auth-tab"
            :class="{ 'active': activeTab === 'register' }"
            @click="activeTab = 'register'"
          >
            Новый покупатель
          </button>
        </div>

        <!-- Форма входа -->
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label for="login-email">Email*</label>
            <input
              id="login-email"
              v-model="loginForm.email"
              type="email"
              placeholder="example@email.com"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="login-password">Пароль*</label>
            <div class="password-input-container">
              <input
                id="login-password"
                v-model="loginForm.password"
                :type="showLoginPassword ? 'text' : 'password'"
                placeholder="Ваш пароль"
                required
                class="form-input"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showLoginPassword = !showLoginPassword"
              >
                <svg v-if="showLoginPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </button>
            </div>
          </div>
          
          <button type="submit" class="auth-button" :disabled="loginLoading">
            {{ loginLoading ? 'Входим...' : 'Войти' }}
          </button>
          
          <div class="auth-footer">
            <p class="auth-notice">
              Нажимая кнопку «Войти» Вы подтверждаете согласие с 
              <a href="/privacy" class="auth-link">Политикой конфиденциальности и защиты персональных данных</a>
              и дает <a href="/consent" class="auth-link">СОГЛАСИЕ</a> на обработку персональных данных
            </p>
          </div>
        </form>
        
        <!-- Форма регистрации -->
        <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="auth-form">
          <div class="form-group">
            <label for="register-email">Email*</label>
            <input
              id="register-email"
              v-model="registerForm.email"
              type="email"
              placeholder="example@email.com"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="register-username">Логин*</label>
            <input
              id="register-username"
              v-model="registerForm.username"
              type="text"
              placeholder="Ваше имя пользователя"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="register-first-name">Имя*</label>
            <input
              id="register-first-name"
              v-model="registerForm.first_name"
              type="text"
              placeholder="Ваше имя"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="register-phone">Телефон</label>
            <input
              id="register-phone"
              v-model="registerForm.phone_number"
              type="tel"
              placeholder="+7 (999) 123-45-67"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="register-address">Адрес</label>
            <textarea
              id="register-address"
              v-model="registerForm.address"
              placeholder="Ваш адрес доставки"
              class="form-input form-textarea"
              rows="2"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="register-password">Пароль*</label>
            <div class="password-input-container">
              <input
                id="register-password"
                v-model="registerForm.password"
                :type="showRegisterPassword ? 'text' : 'password'"
                placeholder="Создайте пароль"
                required
                class="form-input"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showRegisterPassword = !showRegisterPassword"
              >
                <svg v-if="showRegisterPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="register-password-confirm">Подтвердите пароль*</label>
            <input
              id="register-password-confirm"
              v-model="registerForm.passwordConfirm"
              type="password"
              placeholder="Повторите пароль"
              required
              class="form-input"
            />
          </div>
          
          <button type="submit" class="auth-button" :disabled="registerLoading">
            {{ registerLoading ? 'Регистрируем...' : 'Зарегистрироваться' }}
          </button>
          
          <div class="auth-footer">
            <p class="auth-notice">
              Нажимая кнопку «Зарегистрироваться» Покупатель подтверждает согласие с 
              <a href="/privacy" class="auth-link">Политикой конфиденциальности и защиты персональных данных</a>
              и дает <a href="/consent" class="auth-link">СОГЛАСИЕ</a> на обработку персональных данных
            </p>
          </div>
        </form>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close']);

const authStore = useAuthStore();

const activeTab = ref('login');
const showLoginPassword = ref(false);
const showRegisterPassword = ref(false);
const loginLoading = ref(false);
const registerLoading = ref(false);
const errorMessage = ref('');

const loginForm = ref({
  email: '',
  password: ''
});

const registerForm = ref({
  email: '',
  username: '',
  first_name: '',
  phone_number: '',
  address: '',
  password: '',
  passwordConfirm: ''
});

const closeModal = () => {
  emit('close');
  resetForms();
};

const resetForms = () => {
  loginForm.value = { email: '', password: '' };
  registerForm.value = { 
    email: '', 
    username: '', 
    first_name: '', 
    phone_number: '', 
    address: '', 
    password: '', 
    passwordConfirm: '' 
  };
  errorMessage.value = '';
  activeTab.value = 'login';
  showLoginPassword.value = false;
  showRegisterPassword.value = false;
};

const handleLogin = async () => {
  if (loginLoading.value) return;
  
  errorMessage.value = '';
  loginLoading.value = true;
  
  try {

    await authStore.login({
      username: loginForm.value.email,
      password: loginForm.value.password
    });
    
    closeModal();
  } catch (error) {
    console.error('Login error:', error.response?.data);

    if (error.response?.status === 401) {
      errorMessage.value = 'Неверный email или пароль. Проверьте данные и попробуйте снова.';
    } else if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail;
    } else if (error.response?.data?.non_field_errors) {
      errorMessage.value = error.response.data.non_field_errors[0];
    } else {
      errorMessage.value = 'Ошибка входа. Попробуйте еще раз.';
    }
  } finally {
    loginLoading.value = false;
  }
};

const handleRegister = async () => {
  if (registerLoading.value) return;
  
  errorMessage.value = '';

  if (registerForm.value.password !== registerForm.value.passwordConfirm) {
    errorMessage.value = 'Пароли не совпадают';
    return;
  }
  
  registerLoading.value = true;
  
  try {
    await authStore.register({
      username: registerForm.value.username,
      email: registerForm.value.email,
      first_name: registerForm.value.first_name,
      password: registerForm.value.password,
      phone_number: registerForm.value.phone_number,
      address: registerForm.value.address
    });
    await authStore.login({
      username: registerForm.value.email,
      password: registerForm.value.password
    });
    
    closeModal();
  } catch (error) {
    const errors = error.response?.data;
    if (errors) {
      if (errors.email) {
        errorMessage.value = Array.isArray(errors.email) ? errors.email[0] : 'Пользователь с таким email уже существует';
      } else if (errors.username) {
        errorMessage.value = Array.isArray(errors.username) ? errors.username[0] : 'Пользователь с таким именем уже существует';
      } else if (errors.password) {
        errorMessage.value = Array.isArray(errors.password) ? errors.password[0] : 'Ошибка с паролем';
      } else if (errors.first_name) {
        errorMessage.value = Array.isArray(errors.first_name) ? errors.first_name[0] : 'Ошибка с именем';
      } else if (errors.phone_number) {
        errorMessage.value = Array.isArray(errors.phone_number) ? errors.phone_number[0] : 'Ошибка с номером телефона';
      } else if (errors.non_field_errors) {
        errorMessage.value = Array.isArray(errors.non_field_errors) ? errors.non_field_errors[0] : 'Ошибка регистрации';
      } else {
        errorMessage.value = 'Ошибка регистрации. Попробуйте еще раз.';
      }
    } else {
      errorMessage.value = 'Ошибка регистрации. Попробуйте еще раз.';
    }
  } finally {
    registerLoading.value = false;
  }
};

watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    resetForms();
  }
});

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.auth-tabs {
  display: flex;
  border-radius: 50px;
  background-color: #f5f5f5;
  padding: 4px;
  margin-bottom: 2rem;
}

.auth-tab {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.auth-tab.active {
  background-color: #000;
  color: #fff;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
  resize: vertical;
}

.form-textarea {
  min-height: 60px;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #000;
}

.form-input::placeholder {
  color: #999;
}

.password-input-container {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  padding: 0.25rem;
}

.auth-button {
  background-color: #000;
  color: #fff;
  border: none;
  padding: 1rem;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s ease;
  margin-top: 1rem;
}

.auth-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.auth-button:hover:not(:disabled) {
  opacity: 0.9;
}

.auth-footer {
  margin-top: 1rem;
}

.auth-notice {
  font-size: 0.75rem;
  color: #666;
  line-height: 1.4;
  text-align: center;
}

.auth-link {
  color: #000;
  text-decoration: underline;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  margin-top: 1rem;
  text-align: center;
}

@media (max-width: 768px) {
  .modal-content {
    margin: 0.5rem;
    max-height: 95vh;
  }
  
  .modal-header,
  .modal-body {
    padding: 1rem;
  }
}
</style>