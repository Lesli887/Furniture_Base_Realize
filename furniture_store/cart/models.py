from django.db import models
from django.db.models import Sum, Count

from products.models import ProductVariant
from users.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    @property
    def item_count(self):
        """Количество уникальных товаров в корзине (позиций)"""
        return self.items.aggregate(count=Count('id'))['count'] or 0

    @property
    def total_quantity(self):
        """Общее количество товаров (сумма quantity)"""
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0

    @property
    def total_price(self):
        """Общая стоимость корзины"""
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина пользователя {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name='Вариант товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        constraints = [
            models.UniqueConstraint(fields=['cart', 'variant'], name='unique_cart_item')
        ]

    def __str__(self):
        return f"{self.variant.product.name} ({self.variant.color}) - {self.quantity} шт."

    @property
    def total_price(self):
        return self.variant.price * self.quantity
