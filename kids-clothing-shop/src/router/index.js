import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import HomeView from '@/views/HomeView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Главная' }
  },
  {
    path: '/account',
    name: 'account',
    component: () => import('@/views/AccountView.vue'),
    meta: { title: 'Личный кабинет', requiresAuth: true }
  },
  // {
  //   path: '/categories/:gender',
  //   name: 'categories',
  //   component: () => import('@/views/CategoryView.vue'),
  //   meta: { title: 'Категории' }
  // },
  // {
  //   path: '/categories/:gender/:slug',
  //   name: 'category',
  //   component: () => import('@/views/CategoryDetailView.vue'),
  //   meta: { title: 'Категория' }
  // },
  // {
  //   path: '/products/new',
  //   name: 'new-products',
  //   component: () => import('@/views/NewProductsView.vue'),
  //   meta: { title: 'Новинки' }
  // },
  // {
  //   path: '/products/:slug',
  //   name: 'product-detail',
  //   component: () => import('@/views/ProductDetailView.vue'),
  //   meta: { title: 'Товар' }
  // },
  // {
  //   path: '/favorites',
  //   name: 'favorites',
  //   component: () => import('@/views/FavoritesView.vue'),
  //   meta: { title: 'Избранное' }
  // },
  // {
  //   path: '/cart',
  //   name: 'cart',
  //   component: () => import('@/views/CartView.vue'),
  //   meta: { title: 'Корзина' }
  // },
  // {
  //   path: '/checkout',
  //   name: 'checkout',
  //   component: () => import('@/views/CheckoutView.vue'),
  //   meta: { title: 'Оформление заказа' },
  //   // Add basic route guard
  //   beforeEnter: (to, from, next) => {
  //     // Check if cart has items
  //     const cartItems = JSON.parse(localStorage.getItem('cart') || '[]');
  //     if (cartItems.length === 0) {
  //       next({ name: 'cart' });
  //     } else {
  //       next();
  //     }
  //   }
  // },
  // {
  //   path: '/login',
  //   name: 'login',
  //   component: () => import('@/views/LoginView.vue'),
  //   meta: { title: 'Вход' }
  // },
  // {
  //   path: '/register',
  //   name: 'register',
  //   component: () => import('@/views/RegisterView.vue'),
  //   meta: { title: 'Регистрация' }
  // },
  // {
  //   path: '/account',
  //   name: 'account',
  //   component: () => import('@/views/AccountView.vue'),
  //   meta: { title: 'Личный кабинет', requiresAuth: true },
  //   children: [
  //     {
  //       path: 'profile',
  //       name: 'account-profile',
  //       component: () => import('@/views/account/ProfileView.vue'),
  //       meta: { title: 'Профиль', requiresAuth: true }
  //     },
  //     {
  //       path: 'orders',
  //       name: 'account-orders',
  //       component: () => import('@/views/account/OrdersView.vue'),
  //       meta: { title: 'Мои заказы', requiresAuth: true }
  //     }
  //   ]
  // },
  // {
  //   path: '/search',
  //   name: 'search',
  //   component: () => import('@/views/SearchView.vue'),
  //   meta: { title: 'Поиск' }
  // },
  // // Error pages
  // {
  //   path: '/404',
  //   name: 'not-found',
  //   component: () => import('@/views/NotFoundView.vue'),
  //   meta: { title: 'Страница не найдена' }
  // },
  // {
  //   path: '/:pathMatch(.*)*',
  //   redirect: '/404'
  // }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
});

// Navigation guards
// router.beforeEach((to, from, next) => {
//   // Update page title
//   document.title = to.meta.title ? `${to.meta.title} | Kids Clothing Shop` : 'Kids Clothing Shop';
  
//   // Check for protected routes
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     // Check if user is logged in
//     const token = localStorage.getItem('token');
//     if (!token) {
//       next({
//         path: '/login',
//         query: { redirect: to.fullPath }
//       });
//     } else {
//       next();
//     }
//   } else {
//     next();
//   }
// });

router.beforeEach((to, from, next) => {
  // Update page title
  document.title = to.meta.title ? `${to.meta.title} | Kids Clothing Shop` : 'Kids Clothing Shop';
  
  // Check for protected routes
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const authStore = useAuthStore();
    
    if (!authStore.isAuthenticated) {
      // Redirect to home page if not authenticated
      // The user icon will open the login modal
      next('/');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;