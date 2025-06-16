from django.db import models
from django.db.models import Avg
from django.utils.text import slugify


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название цвета')
    hex_code = models.CharField(max_length=7, default='#FFFFFF', verbose_name='HEX код')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name='Изображение категории'
    )
    # Добавляем флаг для показа на главной
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Показывать на главной'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Collection(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(
        upload_to='collections/',
        blank=True,
        null=True,
        verbose_name='Изображение коллекции'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Показывать на главной'
    )

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def products(self):
        return self.product_set.all()


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    is_featured = models.BooleanField(default=False, verbose_name="Показывать в меню")
    collections = models.ManyToManyField(
        Collection,
        blank=True,
        related_name='products',  # Добавьте это
        verbose_name='Коллекции')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Базовая цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True,
                                   verbose_name='Главное изображение')

    @property
    def average_rating(self):
        avg = self.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg']
        return avg if avg else 0.0

    @property
    def default_variant(self):
        try:
            # Пробуем получить вариант по умолчанию
            return self.variants.get(is_default=True)
        except ProductVariant.DoesNotExist:
            # Или первый доступный вариант
            return self.variants.first()

    @property
    def has_stock(self):
        """
        Определяет наличие товара:
        - 'out': нет ни одного варианта в наличии
        - 'partial': есть хотя бы один вариант в наличии, но не все
        - 'full': все варианты в наличии
        """
        variants = self.variants.all()

        if not variants:
            return 'out'

        in_stock_count = variants.filter(stock__gt=0).count()
        total_count = variants.count()

        if in_stock_count == 0:
            return 'out'
        elif in_stock_count < total_count:
            return 'partial'
        else:
            return 'full'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/additional/', verbose_name='Изображение')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name='Описание изображения')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order']

    def __str__(self):
        return f"Изображение для {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='Товар')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Цвет')
    size = models.CharField(max_length=50, blank=True, verbose_name='Размер')
    material = models.CharField(max_length=50, blank=True, verbose_name='Материал')
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Коррекция цены')
    stock = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    is_default = models.BooleanField(default=False, verbose_name='Вариант по умолчанию')

    class Meta:
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товаров'
        ordering = ['-is_default', 'color__name', 'size']

    def __str__(self):
        return f"{self.product.name} - {self.color.name if self.color else 'Без цвета'} - {self.size}"

    def save(self, *args, **kwargs):
        if not self.sku:
            base_sku = slugify(self.product.name).upper()[:20]  # Пример: "MY-PRODUCT"
            variants = ProductVariant.objects.filter(product=self.product).order_by('id')
            next_num = variants.count() + 1 if variants.exists() else 1
            self.sku = f"{base_sku}-{next_num:03d}"  # Пример: "MY-PRODUCT-001"
        super().save(*args, **kwargs)

    @property
    def price(self):
        return self.product.base_price + self.price_modifier


class VariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images', verbose_name='Вариант')
    image = models.ImageField(upload_to='variants/', verbose_name='Изображение')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name='Описание изображения')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        verbose_name = 'Изображение варианта'
        verbose_name_plural = 'Изображения вариантов'
        ordering = ['order']

    def __str__(self):
        return f"Изображение для варианта {self.variant.sku}"
