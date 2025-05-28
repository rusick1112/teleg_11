from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    CustomerProfile, Category, Product, Color, Size,
    ProductVariant, ProductStock, ProductImage, Favorite, Cart, CartItem, Order
)
from .serializers import (
    CustomerProfileSerializer, CategorySerializer, ProductListSerializer, 
    ProductDetailSerializer, ColorSerializer, SizeSerializer,
    ProductVariantSerializer, FavoriteSerializer, CartSerializer, 
    CartItemSerializer, OrderSerializer
)
from .custom_serializers import CustomUserSerializer


class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # Disable pagination for profiles
    
    def get_queryset(self):
        # Get or create profile for the current user
        profile, created = CustomerProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'phone_number': '',
                'address': ''
            }
        )
        return CustomerProfile.objects.filter(user=self.request.user).order_by('id')
    
    def get_object(self):
        # Get or create profile for the current user
        profile, created = CustomerProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'phone_number': '',
                'address': ''
            }
        )
        return profile
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile with enhanced data"""
        profile = self.get_object()
        
        # Return enhanced profile data
        profile_data = {
            'id': profile.id,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            },
            'phone_number': profile.phone_number,
            'address': profile.address,
            # Also include flat structure for easier access
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        
        return Response(profile_data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """Update current user's profile"""
        profile = self.get_object()
        
        # Update user fields if provided
        user = request.user
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data.get('last_name', '')
        user.save()
        
        # Update profile fields
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return the same enhanced format as the me endpoint
        profile_data = {
            'id': profile.id,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            },
            'phone_number': profile.phone_number,
            'address': profile.address,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        
        return Response(profile_data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender', 'parent']
    search_fields = ['name', 'description']
    
    @action(detail=False, methods=['get'])
    def boys(self, request):
        """Все категории товаров для мальчиков"""
        categories = Category.objects.filter(Q(gender='B') | Q(gender='U')).order_by('name')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def girls(self, request):
        """Все категории товаров для девочек"""
        categories = Category.objects.filter(Q(gender='G') | Q(gender='U')).order_by('name')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'categories__gender']
    search_fields = ['title', 'description', 'article']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Optimize queries with prefetch_related
        queryset = Product.objects.filter(is_available=True)
        
        # Prefetch variants with their images and stocks
        variants_prefetch = Prefetch(
            'variants',
            queryset=ProductVariant.objects.prefetch_related(
                Prefetch(
                    'images',
                    queryset=ProductImage.objects.order_by('sort_order')
                ),
                'stocks__size',
                'color'
            )
        )
        
        return queryset.prefetch_related(
            variants_prefetch,
            'categories'
        ).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
    
    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'])
    def boys(self, request):
        """Фильтр для товаров для мальчиков"""
        boy_categories = Category.objects.filter(Q(gender='B') | Q(gender='U'))
        products = self.get_queryset().filter(
            categories__in=boy_categories
        ).distinct()
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def girls(self, request):
        """Фильтр для товаров для девочек"""
        girl_categories = Category.objects.filter(Q(gender='G') | Q(gender='U'))
        products = self.get_queryset().filter(
            categories__in=girl_categories
        ).distinct()
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def variants(self, request, pk=None):
        product = self.get_object()
        variants = product.variants.all().order_by('id')
        serializer = ProductVariantSerializer(variants, many=True, context={'request': request})
        return Response(serializer.data)


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.all().order_by('name')
    serializer_class = ColorSerializer


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Size.objects.all().order_by('display_order')
    serializer_class = SizeSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-added_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {'error': 'Нужен id товара'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product = get_object_or_404(Product, id=product_id)
        favorite = Favorite.objects.filter(user=request.user, product=product).first()
        
        if favorite:
            favorite.delete()
            return Response({'status': 'удалён'}, status=status.HTTP_200_OK)
        else:
            Favorite.objects.create(user=request.user, product=product)
            return Response({'status': 'добавлен'}, status=status.HTTP_201_CREATED)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user).order_by('-updated_at')
        
        session_id = self.request.session.session_key
        if not session_id:
            self.request.session.create()
            session_id = self.request.session.session_key
        
        return Cart.objects.filter(session_id=session_id).order_by('-updated_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_object(self):
        queryset = self.get_queryset()
        cart = queryset.first()
        
        if not cart:
            # Создание новой корзины
            if self.request.user.is_authenticated:
                cart = Cart.objects.create(user=self.request.user)
            else:
                session_id = self.request.session.session_key
                cart = Cart.objects.create(session_id=session_id)
        
        return cart
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def merge(self, request):
        """Сохранение корзины анонимного пользователя после авторизации"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Вы должны быть зарегестрированы'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        session_id = request.session.session_key
        if not session_id:
            return Response({'message': 'Нет добавленных товаров'})
        
        # Поиск товаров в корзине до регистрации
        anonymous_cart = Cart.objects.filter(session_id=session_id).first()
        if not anonymous_cart or not anonymous_cart.items.exists():
            return Response({'message': 'Нет добавленных товаров'})
        
        # Поиск/создание корзины
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Сохранение корзины анонимного пользователя после авторизации
        for anon_item in anonymous_cart.items.all():
            # Проверка товара на сущестовавание товара в корзине
            user_item = user_cart.items.filter(
                product_stock=anon_item.product_stock
            ).first()
            
            if user_item:
                # Увелечение количества товаров
                user_item.quantity += anon_item.quantity
                user_item.save()
            else:
                # Добавление товара в корзину
                anon_item.cart = user_cart
                anon_item.save()
        
        # Удаление корзины не зарегистрированного пользователя
        anonymous_cart.delete()
        
        # Обновление корзины пользователя
        serializer = self.get_serializer(user_cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        cart = self.get_cart()
        return CartItem.objects.filter(cart=cart).order_by('-added_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_cart(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_id = self.request.session.session_key
            if not session_id:
                self.request.session.create()
                session_id = self.request.session.session_key
            
            cart, created = Cart.objects.get_or_create(session_id=session_id)
        
        return cart
    
    def create(self, request, *args, **kwargs):
        cart = self.get_cart()
        
        # Добавить информацию о корзине для запроса 
        mutable_data = request.data.copy()
        
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        
        # Проверка существует ли товар в корзине
        product_stock_id = serializer.validated_data['product_stock'].id
        existing_item = CartItem.objects.filter(
            cart=cart, 
            product_stock_id=product_stock_id
        ).first()
        
        if existing_item:
            # Увеличеть количество
            existing_item.quantity += serializer.validated_data.get('quantity', 1)
            existing_item.save()
            response_serializer = self.get_serializer(existing_item)
            return Response(response_serializer.data)
        
        # Create new item
        serializer.save(cart=cart)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def create(self, request, *args, **kwargs):
        # Получение текущей корзины
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'No cart found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создание заказа
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(
            user=request.user,
            total_price=cart.total_price
        )
        
        # Создание товаров в заказе из корзины
        for cart_item in cart.items.all():
            product_stock = cart_item.product_stock
            product = product_stock.variant.product
            variant = product_stock.variant
            size = product_stock.size
            price = product.sale_price if product.sale_price else product.price
            
            # Создание товаров в заказе
            order.items.create(
                product=product,
                variant=variant,
                size=size,
                price=price,
                quantity=cart_item.quantity
            )
        
        # Очистка корзины
        cart.items.all().delete()
        
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )