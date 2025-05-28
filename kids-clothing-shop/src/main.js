import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/authStore'
import { useFavoriteStore } from './stores/favoriteStore'
import './assets/css/variables.css'
import './assets/css/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

const initializeStores = async () => {
  const { useAuthStore } = await import('./stores/authStore')
  const { useFavoriteStore } = await import('./stores/favoriteStore')
  
  const authStore = useAuthStore()
  const favoriteStore = useFavoriteStore()
  
  // Initialize auth first
  await authStore.initializeAuth()
  
  // Then load favorites if user is authenticated
  if (authStore.isAuthenticated) {
    try {
      await favoriteStore.loadFavoritesFromAPI()
    } catch (error) {
      console.error('Failed to load favorites:', error)
    }
  }
}

// Initialize stores and then mount the app
initializeStores().then(() => {
  app.mount('#app')
}).catch(error => {
  console.error('Failed to initialize stores:', error)
  // Mount the app anyway
  app.mount('#app')
})