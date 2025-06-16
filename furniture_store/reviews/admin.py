from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'title')
    list_editable = ('is_approved',)
    fieldsets = (
        (None, {
            'fields': ('product', 'user', 'rating', 'title', 'text')
        }),
        ('Модерация', {
            'fields': ('is_approved',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'user')