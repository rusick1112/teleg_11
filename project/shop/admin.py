from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

# прокси модель для профиля
class EmployeeInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = "Информация"

class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# категория товаров
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'gender')
    list_filter = ('gender',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# вариация под похожие(одинаковая серия) товары
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'is_default')
    list_filter = ('color', 'is_default')
    search_fields = ('product__title', 'color__name')
    inlines = [ProductImageInline, ProductStockInline]

# товар
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'price', 'sale_price', 'is_available', 'created_at')
    list_filter = ('is_available', 'categories')
    search_fields = ('title', 'article', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    list_editable = ('price', 'sale_price', 'is_available')
    date_hierarchy = 'created_at'

# цвета
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name',)

# размерная сетка
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = ('display_order',)

# изображение товара
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('variant', 'alt_text', 'sort_order')
    list_filter = ('variant__product',)
    search_fields = ('variant__product__title', 'alt_text')

# 
@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('get_product', 'get_color', 'size', 'quantity')
    list_filter = ('variant__product', 'variant__color', 'size')
    search_fields = ('variant__product__title',)
    list_editable = ('quantity',)
    
    def get_product(self, obj):
        return obj.variant.product.title
    get_product.short_description = 'Product'
    
    def get_color(self, obj):
        return obj.variant.color.name
    get_color.short_description = 'Color'

# любимые товары
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__title')
    date_hierarchy = 'added_at'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

# Корзина
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'created_at', 'updated_at', 'get_total_price')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_id')
    date_hierarchy = 'created_at'
    inlines = [CartItemInline]
    
    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = 'Total Price'

# Товары в корзине
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'get_product', 'get_color', 'get_size', 'quantity', 'added_at')
    list_filter = ('added_at', 'product_stock__variant__product')
    search_fields = ('cart__user__username', 'product_stock__variant__product__title')
    list_editable = ('quantity',)
    
    def get_product(self, obj):
        return obj.product_stock.variant.product.title
    get_product.short_description = 'Товар'
    
    def get_color(self, obj):
        return obj.product_stock.variant.color.name
    get_color.short_description = 'Цвет'
    
    def get_size(self, obj):
        return obj.product_stock.size.name
    get_size.short_description = 'Размер'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# Заказ
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'email', 'phone', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'full_name', 'email', 'phone')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]