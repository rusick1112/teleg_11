import axios from 'axios';

// Create an axios instance with default configurations
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true // Enable cookies for session-based authentication
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle common errors
apiClient.interceptors.response.use(
  response => response,
  error => {
    // Handle token expiration
    if (error.response?.status === 401) {
      // Clear tokens and redirect to login if token is invalid or expired
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      
      // Only redirect to login if not already there
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }
    
    // Handle other errors
    return Promise.reject(error);
  }
);

export default {
  // Authentication
  login(credentials) {
    return apiClient.post('/token/', credentials);
  },
  
  refreshToken(refreshToken) {
    return apiClient.post('/token/refresh/', { refresh: refreshToken });
  },
  
  register(userData) {
    return apiClient.post('/auth/users/', userData);
  },
  
  // Profile
  getUserProfile() {
    return apiClient.get('/profiles/');
  },
  
  updateUserProfile(profileData) {
    return apiClient.put('/profiles/', profileData);
  },
  
  // Products
  getProducts(params = {}) {
    return apiClient.get('/products/', { params });
  },
  
  getProductById(id) {
    return apiClient.get(`/products/${id}/`);
  },
  
  getProductBySlug(slug) {
    return apiClient.get(`/products/${slug}/`);
  },
  
  getBoysProducts(params = {}) {
    return apiClient.get('/products/boys/', { params });
  },
  
  getGirlsProducts(params = {}) {
    return apiClient.get('/products/girls/', { params });
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
  
  // Favorites
  getFavorites() {
    return apiClient.get('/favorites/');
  },
  
  toggleFavorite(productId) {
    return apiClient.post('/favorites/toggle/', { product_id: productId });
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
  
  // Orders
  getOrders() {
    return apiClient.get('/orders/');
  },
  
  getOrderById(id) {
    return apiClient.get(`/orders/${id}/`);
  },
  
  createOrder(orderData) {
    return apiClient.post('/orders/', orderData);
  },
  
  // Search
  search(query) {
    return apiClient.get('/products/', { params: { search: query } });
  }
};