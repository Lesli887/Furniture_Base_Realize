from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product
from users.models import User

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Рейтинг'
    )
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = [['product', 'user']]

    def __str__(self):
        return f"Отзыв на {self.product.name} от {self.user.email}"