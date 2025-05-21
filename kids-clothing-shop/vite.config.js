// vite.config.js
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import path from 'node:path'  // Import path module from Node.js

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 3000,
    proxy: {
      // Proxy API requests to your Django backend server
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        ws: true,
        // Uncomment if your API doesn't have /api prefix on the backend
        // rewrite: (path) => path.replace(/^\/api/, '')
      },
      // Proxy media files
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      },
      // Proxy static files
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
});