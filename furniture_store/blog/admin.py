from django.contrib import admin
from .models import Tag, Post


class PostInline(admin.TabularInline):
    model = Post.tags.through
    extra = 1
    verbose_name = 'Пост'
    verbose_name_plural = 'Посты'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    inlines = [PostInline]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'tags', 'created_at')
    readonly_fields = ('formatted_content',)
    search_fields = ('title', 'content', 'author__email')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'author', 'image')
        }),
        ('Метаданные', {
            'fields': ('tags', 'is_published'),  # Добавьте поле
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')