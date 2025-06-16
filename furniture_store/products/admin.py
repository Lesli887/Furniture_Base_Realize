from django.contrib import admin
from image_uploader_widget.admin import ImageUploaderInline
from image_uploader_widget.widgets import ImageUploaderWidget

from .models import Category, Collection, Product, ProductVariant, Color, ProductImage, VariantImage
from django import forms


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('color', 'size', 'material', 'sku', 'price_modifier', 'stock', 'price')
    readonly_fields = ('price',)

    @admin.display(description='Цена')
    def price(self, instance):
        return instance.price


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)



class VariantImageInline(ImageUploaderInline):
    model = VariantImage
    


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    list_display = ('name', 'category', 'base_price', 'created_at')
    list_filter = ('category', 'collections')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('collections',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [VariantImageInline]  # Добавляем VariantImageInline
    list_display = ('product', 'color', 'size', 'material', 'sku', 'price', 'stock', 'is_default')
    list_filter = ('product__category', 'color', 'size', 'material')
    search_fields = ('sku', 'product__name')
    readonly_fields = ('price',)

    @admin.display(description='Цена')
    def price(self, obj):
        return obj.price
