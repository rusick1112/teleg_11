import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      // Proxy API requests to your backend server
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        // Uncomment if your API doesn't have /api prefix on the backend
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
});