from django.contrib import admin
from .models import Category, Product, ProductImage, Address, Cart, CartItem, Order, OrderItem, Review, Banner

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_featured', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'brand', 'price', 'original_price', 'stock', 'is_prime', 'is_deal_of_the_day', 'rating')
    list_filter = ('category', 'brand', 'is_prime', 'is_deal_of_the_day')
    search_fields = ('title', 'brand', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_title', 'price', 'quantity', 'item_subtotal')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'full_name', 'email', 'mobile', 'total_amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_id', 'full_name', 'email', 'mobile')
    inlines = [OrderItemInline]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'town_city', 'pincode', 'mobile_number', 'is_default')
    search_fields = ('full_name', 'pincode', 'town_city')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'verified_purchase')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_text', 'is_active', 'created_at')
    list_editable = ('is_active',)

admin.site.register(Cart)
admin.site.register(CartItem)
