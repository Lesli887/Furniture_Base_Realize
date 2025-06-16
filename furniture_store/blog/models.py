import bleach
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    content = RichTextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def formatted_content(self):
        return format_html(self.content)

    formatted_content.short_description = 'Превью содержания'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Убедитесь, что очистка HTML не удаляет нужные теги
        self.content = bleach.clean(
            self.content,
            tags=settings.ALLOWED_HTML_TAGS,
            attributes=settings.ALLOWED_HTML_ATTRIBUTES
        )
        super().save(*args, **kwargs)