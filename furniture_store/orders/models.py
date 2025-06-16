from django.db import models
from products.models import ProductVariant, Product
from users.models import User
from django.core.validators import MinValueValidator


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('failed', 'Ошибка оплаты'),
        ('refunded', 'Возврат'),
    ]

    # Новое поле: выбор способа оплаты
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Оплата онлайн'),
        ('upon_receipt', 'Оплата при получении'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='Статус оплаты'
    )
    # Новое поле для хранения способа оплаты
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='online',
        verbose_name='Способ оплаты'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая сумма')
    address = models.TextField(verbose_name='Адрес доставки')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    # Поля для Stripe
    stripe_id = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='ID платежа Stripe'
    )
    stripe_payment_intent = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='ID платежного намерения Stripe'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.created_at.strftime('%d.%m.%Y')}"

    @property
    def is_paid(self):
        # Для оплаты при получении считаем заказ "условно оплаченным"
        if self.payment_method == 'upon_receipt':
            return self.payment_status in ['paid', 'pending']
        return self.payment_status == 'paid'

    def save(self, *args, **kwargs):
        # Автоматически обновляем статус оплаты для "Оплаты при получении"
        if self.payment_method == 'upon_receipt' and self.payment_status == 'pending':
            # Можно добавить дополнительную логику обработки
            pass
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, verbose_name='Вариант товара')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    name = models.CharField(max_length=255, verbose_name='Название товара')
    sku = models.CharField(max_length=50, verbose_name='Артикул')

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Товар'
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f"{self.name} - {self.quantity} шт."

    @property
    def total(self):
        return self.price * self.quantity