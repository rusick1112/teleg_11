from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerProfileViewSet, CategoryViewSet, ProductViewSet,
    ColorViewSet, SizeViewSet, FavoriteViewSet,
    CartViewSet, CartItemViewSet, OrderViewSet
)

router = DefaultRouter()
router.register(r'profiles', CustomerProfileViewSet, basename='profile')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'colors', ColorViewSet, basename='color')
router.register(r'sizes', SizeViewSet, basename='size')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]