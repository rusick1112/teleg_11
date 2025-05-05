from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CustomerProfile(models.Model):
    """Proxy model for extending the User model with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Category(models.Model):
    """Category model for organizing products"""
    GENDER_CHOICES = (
        ('B', 'Boys'),
        ('G', 'Girls'),
        ('U', 'Unisex'),
    )
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    image = models.ImageField(upload_to='categories', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Main product model for clothing items"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    article = models.CharField(max_length=50, unique=True, help_text="Unique product identifier/code")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='products')
    description = models.TextField()
    composition = models.CharField(max_length=255, blank=True, help_text="E.g. Cotton 95%, Elastane 5%")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def main_image(self):
        """Return the first image for this product"""
        product_variant = self.variants.first()
        if product_variant and product_variant.images.exists():
            return product_variant.images.first()
        return None
    
    @property
    def available_colors(self):
        """Return a list of all available colors for this product"""
        return list(self.variants.values_list('color', flat=True).distinct())


class Color(models.Model):
    """Color options for products"""
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, help_text="Color code (e.g., HEX #FFFFFF)")
    
    def __str__(self):
        return self.name


class Size(models.Model):
    """Size options for products"""
    name = models.CharField(max_length=20)  # XS, S, M, L, XL or numeric sizes like 110, 116, etc.
    display_order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Variant of a product with specific color and available sizes"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size, through='ProductStock')
    is_default = models.BooleanField(default=False, help_text="Is this the default variant shown for the product")
    
    class Meta:
        unique_together = [['product', 'color']]
    
    def __str__(self):
        return f"{self.product.title} - {self.color.name}"


class ProductImage(models.Model):
    """Images for product variants"""
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
    
    def __str__(self):
        return f"Image for {self.variant}"


class ProductStock(models.Model):
    """Stock keeping unit for each product variant and size combination"""
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stocks')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = [['variant', 'size']]
    
    def __str__(self):
        return f"{self.variant.product.title} - {self.variant.color.name} - {self.size.name}"


class Favorite(models.Model):
    """User favorites"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['user', 'product']]
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


class Cart(models.Model):
    """Shopping cart model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id} - {'User: ' + self.user.username if self.user else 'Anonymous'}"
    
    @property
    def total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    """Individual items in a cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['cart', 'product_stock']]
    
    def __str__(self):
        product = self.product_stock.variant.product
        color = self.product_stock.variant.color
        size = self.product_stock.size
        return f"{product.title} - {color.name} - {size.name} x {self.quantity}"
    
    def get_total_price(self):
        product = self.product_stock.variant.product
        price = product.sale_price if product.sale_price else product.price
        return price * self.quantity


class Order(models.Model):
    """Order model to track completed purchases"""
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.full_name}"


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.title} - {self.variant.color.name} - {self.size.name} x {self.quantity}"