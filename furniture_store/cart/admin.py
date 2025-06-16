from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ('variant', 'quantity', 'added_at')
    readonly_fields = ('added_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'items_count')
    list_select_related = ('user',)
    inlines = [CartItemInline]
    search_fields = ('user__email',)

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = 'Товаров'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'variant', 'quantity', 'added_at')
    list_filter = ('cart__user',)
    search_fields = ('variant__product__name', 'variant__color')
    readonly_fields = ('added_at',)