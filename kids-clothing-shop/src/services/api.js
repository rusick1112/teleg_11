import axios from 'axios';

// With Vite proxy, we can use relative URLs
// The proxy in vite.config.js will forward these to the actual backend
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Add interceptor for auth tokens
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  // Products
  getProducts(params = {}) {
    return apiClient.get('/products/', { params });
  },
  getProductById(id) {
    return apiClient.get(`/products/${id}/`);
  },
  getBoysProducts() {
    return apiClient.get('/products/boys/');
  },
  getGirlsProducts() {
    return apiClient.get('/products/girls/');
  },
  
  // Categories
  getCategories() {
    return apiClient.get('/categories/');
  },
  getBoysCategories() {
    return apiClient.get('/categories/boys/');
  },
  getGirlsCategories() {
    return apiClient.get('/categories/girls/');
  },
  
  // Cart
  getCurrentCart() {
    return apiClient.get('/carts/current/');
  },
  addToCart(data) {
    return apiClient.post('/cart-items/', data);
  },
  updateCartItem(id, data) {
    return apiClient.put(`/cart-items/${id}/`, data);
  },
  removeCartItem(id) {
    return apiClient.delete(`/cart-items/${id}/`);
  },
  
  // Favorites
  getFavorites() {
    return apiClient.get('/favorites/');
  },
  toggleFavorite(productId) {
    return apiClient.post('/favorites/toggle/', { product_id: productId });
  },
  
  // Auth
  login(credentials) {
    return apiClient.post('/token/', credentials);
  },
  register(userData) {
    return apiClient.post('/auth/users/', userData);
  },
}