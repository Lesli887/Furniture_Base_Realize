from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('variant', 'quantity', 'price', 'total', 'name', 'sku')
    readonly_fields = ('price', 'total', 'name', 'sku')

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'phone', 'address')
    readonly_fields = ('user', 'total', 'created_at')
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'total', 'created_at')
        }),
        ('Информация о доставке', {
            'fields': ('address', 'phone', 'email', 'comment')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'quantity', 'price', 'total')
    list_filter = ('order__status',)
    search_fields = ('name', 'sku', 'order__id')
    readonly_fields = ('order', 'variant', 'quantity', 'price', 'name', 'sku', 'total')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False