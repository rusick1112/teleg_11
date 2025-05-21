from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    CustomerProfile, Category, Product, Color, Size,
    ProductVariant, ProductImage, ProductStock,
    Favorite, Cart, CartItem, Order, OrderItem
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'phone_number', 'address']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'gender', 'image']
        read_only_fields = ['id', 'slug']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'code']
        read_only_fields = ['id']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name', 'display_order']
        read_only_fields = ['id']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'sort_order']
        read_only_fields = ['id']


class ProductStockSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True)
    size_id = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(), 
        source='size',
        write_only=True
    )
    
    class Meta:
        model = ProductStock
        fields = ['id', 'size', 'size_id', 'quantity']
        read_only_fields = ['id']


class ProductVariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(),
        source='color',
        write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    stocks = ProductStockSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'color', 'color_id', 'is_default', 'images', 'stocks']
        read_only_fields = ['id']


class ProductListSerializer(serializers.ModelSerializer):
    main_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'article', 'price', 
            'sale_price', 'main_image_url', 'is_available'
        ]
        read_only_fields = ['id', 'slug']
    
    def get_main_image_url(self, obj):
        if obj.main_image and hasattr(obj.main_image, 'image'):
            return obj.main_image.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='categories',
        write_only=True,
        many=True
    )
    variants = ProductVariantSerializer(many=True, read_only=True)
    available_colors = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'article', 'price', 'sale_price',
            'categories', 'category_ids', 'description', 'composition',
            'is_available', 'variants', 'available_colors',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'available_colors', 'created_at', 'updated_at']
    
    def get_available_colors(self, obj):
        variants = obj.variants.all()
        colors = [variant.color for variant in variants]
        return ColorSerializer(colors, many=True).data


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'product_id', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product_stock = ProductStockSerializer(read_only=True)
    product_stock_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductStock.objects.all(),
        source='product_stock',
        write_only=True
    )
    product_info = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_stock', 'product_stock_id', 'quantity', 'product_info', 'added_at']
        read_only_fields = ['id', 'added_at', 'product_info']
    
    def get_product_info(self, obj):
        product = obj.product_stock.variant.product
        variant = obj.product_stock.variant
        size = obj.product_stock.size
        
        return {
            'product_id': product.id,
            'title': product.title,
            'price': float(product.sale_price if product.sale_price else product.price),
            'color': variant.color.name,
            'size': size.name,
            'image': variant.images.first().image.url if variant.images.exists() else None,
            'total_price': float(obj.get_total_price())
        }


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'total_price', 'created_at', 'updated_at']
    
    def get_total_price(self, obj):
        return float(obj.total_price)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'variant', 'size', 'price', 'quantity']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'full_name', 'email', 'phone', 'address',
            'total_price', 'status', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']