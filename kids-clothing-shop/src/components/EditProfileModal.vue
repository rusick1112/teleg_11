<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">Редактировать профиль</h2>
        <button class="close-button" @click="closeModal">×</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="handleSubmit" class="edit-form">
          <div class="form-group">
            <label for="edit-username">Имя пользователя</label>
            <input
              id="edit-username"
              v-model="formData.username"
              type="text"
              placeholder="Ваш логин"
              disabled
              class="form-input disabled"
            />
            <small class="field-note">Логин нельзя изменить</small>
          </div>
          
          <div class="form-group">
            <label for="edit-email">Email</label>
            <input
              id="edit-email"
              v-model="formData.email"
              type="email"
              placeholder="example@email.com"
              disabled
              class="form-input disabled"
            />
            <small class="field-note">Email нельзя изменить</small>
          </div>
          
          <div class="form-group">
            <label for="edit-first-name">Имя*</label>
            <input
              id="edit-first-name"
              v-model="formData.first_name"
              type="text"
              placeholder="Ваше имя"
              required
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="edit-phone">Телефон</label>
            <input
              id="edit-phone"
              v-model="formData.phone_number"
              type="tel"
              placeholder="+7 (999) 123-45-67"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="edit-address">Адрес</label>
            <textarea
              id="edit-address"
              v-model="formData.address"
              placeholder="Ваш адрес доставки"
              class="form-input form-textarea"
              rows="3"
            ></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="closeModal" class="cancel-button">
              Отмена
            </button>
            <button type="submit" class="save-button" :disabled="loading">
              {{ loading ? 'Сохраняем...' : 'Сохранить' }}
            </button>
          </div>
        </form>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'updated']);

const authStore = useAuthStore();
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const formData = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone_number: '',
  address: ''
});

// Подтягивание информации текущего пользователя
const initializeForm = () => {
  const profile = authStore.userProfile;
  if (profile) {
    formData.value = {
      username: profile.username || profile.user?.username || '',
      email: profile.email || profile.user?.email || '',
      first_name: profile.first_name || profile.user?.first_name || '',
      last_name: profile.last_name || profile.user?.last_name || '',
      phone_number: profile.phone_number || '',
      address: profile.address || ''
    };
  }
};

// Проверка на изминение содержимого формы
const hasChanges = computed(() => {
  const profile = authStore.userProfile;
  if (!profile) return false;
  
  return (
    formData.value.first_name !== (profile.first_name || profile.user?.first_name || '') ||
    formData.value.last_name !== (profile.last_name || profile.user?.last_name || '') ||
    formData.value.phone_number !== (profile.phone_number || '') ||
    formData.value.address !== (profile.address || '')
  );
});

const closeModal = () => {
  if (hasChanges.value) {
    if (confirm('У вас есть несохраненные изменения. Вы уверены, что хотите закрыть форму?')) {
      emit('close');
      resetForm();
    }
  } else {
    emit('close');
    resetForm();
  }
};

const resetForm = () => {
  errorMessage.value = '';
  successMessage.value = '';
  initializeForm();
};

const handleSubmit = async () => {
  if (loading.value) return;
  
  errorMessage.value = '';
  successMessage.value = '';
  loading.value = true;
  
  try {
    // Поля доступные для изменения
    const updateData = {
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      phone_number: formData.value.phone_number,
      address: formData.value.address
    };
    
    await authStore.updateProfile(updateData);
    
    successMessage.value = 'Профиль успешно обновлен!';
    emit('updated');

    setTimeout(() => {
      emit('close');
      resetForm();
    }, 1500);
    
  } catch (error) {
    console.error('Profile update error:', error);
    
    const errors = error.response?.data;
    if (errors) {
      if (errors.first_name) {
        errorMessage.value = Array.isArray(errors.first_name) ? errors.first_name[0] : 'Ошибка с именем';
      } else if (errors.last_name) {
        errorMessage.value = Array.isArray(errors.last_name) ? errors.last_name[0] : 'Ошибка с фамилией';
      } else if (errors.phone_number) {
        errorMessage.value = Array.isArray(errors.phone_number) ? errors.phone_number[0] : 'Ошибка с номером телефона';
      } else if (errors.address) {
        errorMessage.value = Array.isArray(errors.address) ? errors.address[0] : 'Ошибка с адресом';
      } else if (errors.non_field_errors) {
        errorMessage.value = Array.isArray(errors.non_field_errors) ? errors.non_field_errors[0] : 'Ошибка обновления профиля';
      } else {
        errorMessage.value = 'Ошибка обновления профиля. Попробуйте еще раз.';
      }
    } else {
      errorMessage.value = 'Ошибка обновления профиля. Попробуйте еще раз.';
    }
  } finally {
    loading.value = false;
  }
};

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    initializeForm();
  } else {
    resetForm();
  }
});

watch(() => authStore.userProfile, () => {
  if (props.isOpen) {
    initializeForm();
  }
}, { deep: true });
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
  max-width: 500px;
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

.edit-form {
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

.form-input:focus {
  outline: none;
  border-color: #000;
}

.form-input.disabled {
  background-color: #f5f5f5;
  color: #666;
  cursor: not-allowed;
}

.form-textarea {
  min-height: 80px;
  font-family: inherit;
}

.field-note {
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: #666;
  font-style: italic;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.cancel-button {
  padding: 0.75rem 1.5rem;
  border: 1px solid #e0e0e0;
  background-color: #fff;
  color: #333;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.cancel-button:hover {
  background-color: #f5f5f5;
}

.save-button {
  padding: 0.75rem 1.5rem;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s ease;
}

.save-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.save-button:hover:not(:disabled) {
  opacity: 0.9;
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

.success-message {
  background-color: #efe;
  color: #2a7f3e;
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
  
  .form-actions {
    flex-direction: column;
  }
  
  .cancel-button,
  .save-button {
    width: 100%;
  }
}
</style>