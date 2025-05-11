from django.contrib import admin
from .models import Category, Product, Review, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'created_at']
    list_filter = ['category', 'brand', 'created_at']
    search_fields = ['name', 'code', 'description']
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
