from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    CustomerProfile, Category, Product, Color, Size,
    ProductVariant, ProductStock, Favorite, Cart, CartItem, Order
)
from .serializers import (
    CustomerProfileSerializer, CategorySerializer, ProductListSerializer, 
    ProductDetailSerializer, ColorSerializer, SizeSerializer,
    ProductVariantSerializer, FavoriteSerializer, CartSerializer, 
    CartItemSerializer, OrderSerializer
)


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own profile
        return CustomerProfile.objects.filter(user=self.request.user)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender', 'parent']
    search_fields = ['name', 'description']
    
    @action(detail=False, methods=['get'])
    def boys(self, request):
        """Get all boys categories"""
        categories = Category.objects.filter(Q(gender='B') | Q(gender='U'))
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def girls(self, request):
        """Get all girls categories"""
        categories = Category.objects.filter(Q(gender='G') | Q(gender='U'))
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'categories__gender']
    search_fields = ['title', 'description', 'article']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
    
    @action(detail=False, methods=['get'])
    def boys(self, request):
        """Get all boys products"""
        boy_categories = Category.objects.filter(Q(gender='B') | Q(gender='U'))
        products = Product.objects.filter(categories__in=boy_categories, is_available=True).distinct()
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def girls(self, request):
        """Get all girls products"""
        girl_categories = Category.objects.filter(Q(gender='G') | Q(gender='U'))
        products = Product.objects.filter(categories__in=girl_categories, is_available=True).distinct()
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def variants(self, request, pk=None):
        product = self.get_object()
        variants = product.variants.all()
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Size.objects.all().order_by('display_order')
    serializer_class = SizeSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {'error': 'Product ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product = get_object_or_404(Product, id=product_id)
        favorite = Favorite.objects.filter(user=request.user, product=product).first()
        
        if favorite:
            favorite.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)
        else:
            Favorite.objects.create(user=request.user, product=product)
            return Response({'status': 'added'}, status=status.HTTP_201_CREATED)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        
        session_id = self.request.session.session_key
        if not session_id:
            self.request.session.create()
            session_id = self.request.session.session_key
        
        return Cart.objects.filter(session_id=session_id)
    
    def get_object(self):
        queryset = self.get_queryset()
        cart = queryset.first()
        
        if not cart:
            # Create a new cart
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
        """Merge anonymous cart with user cart after login"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'You must be logged in to merge carts'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        session_id = request.session.session_key
        if not session_id:
            return Response({'message': 'No anonymous cart to merge'})
        
        # Find anonymous cart
        anonymous_cart = Cart.objects.filter(session_id=session_id).first()
        if not anonymous_cart or not anonymous_cart.items.exists():
            return Response({'message': 'No anonymous cart to merge'})
        
        # Find or create user cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Move items from anonymous cart to user cart
        for anon_item in anonymous_cart.items.all():
            # Check if this item already exists in user cart
            user_item = user_cart.items.filter(
                product_stock=anon_item.product_stock
            ).first()
            
            if user_item:
                # Update quantity
                user_item.quantity += anon_item.quantity
                user_item.save()
            else:
                # Move item to user cart
                anon_item.cart = user_cart
                anon_item.save()
        
        # Delete anonymous cart
        anonymous_cart.delete()
        
        # Return updated user cart
        serializer = self.get_serializer(user_cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        cart = self.get_cart()
        return CartItem.objects.filter(cart=cart)
    
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
        
        # Add cart info to request data
        mutable_data = request.data.copy()
        
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        
        # Check if item already exists in cart
        product_stock_id = serializer.validated_data['product_stock'].id
        existing_item = CartItem.objects.filter(
            cart=cart, 
            product_stock_id=product_stock_id
        ).first()
        
        if existing_item:
            # Update quantity
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
        return Order.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Get current cart
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
        
        # Create order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(
            user=request.user,
            total_price=cart.total_price
        )
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            product_stock = cart_item.product_stock
            product = product_stock.variant.product
            variant = product_stock.variant
            size = product_stock.size
            price = product.sale_price if product.sale_price else product.price
            
            # Create order item
            order.items.create(
                product=product,
                variant=variant,
                size=size,
                price=price,
                quantity=cart_item.quantity
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )