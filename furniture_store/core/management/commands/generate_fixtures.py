import random
import os
import io
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from products.models import Category, Collection, Product, ProductVariant, ProductImage, VariantImage, Color
from blog.models import Tag, Post
from reviews.models import Review
from users.models import Profile
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from datetime import datetime, timedelta
import lorem
import uuid
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings


def generate_unique_slug(model, name, max_length=100):
    base_slug = slugify(name)[:max_length].strip('-')
    if not base_slug:
        base_slug = str(uuid.uuid4())[:8]

    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        if len(slug) > max_length:
            slug = slug[:max_length]
        counter += 1

    return slug


def create_dummy_image(width=800, height=600, color=(200, 200, 200), text="Image"):
    """Создает фиктивное изображение из реальных файлов"""
    # Путь к папке с изображениями
    image_dir = os.path.join(settings.BASE_DIR, 'fixture_images')

    # Проверяем существование директории
    if os.path.exists(image_dir):
        images = [f for f in os.listdir(image_dir)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if images:
            # Выбираем случайное изображение
            img_name = random.choice(images)
            img_path = os.path.join(image_dir, img_name)

            # Читаем содержимое файла в память
            with open(img_path, 'rb') as f:
                content = io.BytesIO(f.read())
            return File(content, name=img_name)

    if "Category" in text:
        text = f"Категория: {text.split(' ')[1]}"
    elif "Collection" in text:
        text = f"Коллекция: {text.split(' ')[1]}"
    elif "Product" in text:
        text = f"Товар: {text.split(' ')[1]}"

    # Если изображений нет - создаем стандартную заглушку
    image = Image.new('RGB', (width, height), color)
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except IOError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(image)
    text_width = draw.textlength(text, font=font)
    text_height = font.size
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, fill=(0, 0, 0), font=font)

    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)  # Важно: переводим указатель в начало файла
    return File(image_io, name=f'dummy_{text}.jpg')


class Command(BaseCommand):
    help = 'Generates comprehensive test data for the furniture store'

    def handle(self, *args, **options):
        self.stdout.write("Starting data generation...")

        # Очищаем базу данных перед созданием новых данных
        self.stdout.write("Deleting old data...")
        self.delete_all_data()

        # Создаем цвета
        colors = self.create_colors()

        # Создаем пользователей
        users = self.create_users()

        # Создаем категории
        categories = self.create_categories()

        # Создаем коллекции
        collections = self.create_collections()

        # Создаем товары
        products = self.create_products(categories, collections, colors)

        # Создаем теги
        tags = self.create_tags()

        # Создаем посты блога
        self.create_blog_posts(users, tags)

        # Создаем отзывы
        self.create_reviews(products, users)

        # Создаем корзины
        self.create_carts(users)

        # Создаем заказы
        self.create_orders(users)

        # Добавляем избранное
        self.add_favorites(users, products)

        self.stdout.write(self.style.SUCCESS('Successfully generated test data!'))

    def delete_all_data(self):
        # Важно соблюдать порядок удаления из-за зависимостей
        # Начинаем с зависимых объектов
        VariantImage.objects.all().delete()
        ProductImage.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Review.objects.all().delete()
        Post.objects.all().delete()
        Tag.objects.all().delete()
        ProductVariant.objects.all().delete()
        Product.objects.all().delete()
        Collection.objects.all().delete()
        Category.objects.all().delete()
        Color.objects.all().delete()
        Profile.objects.all().delete()  # Удаляем профили перед пользователями

        # Удаляем пользователей
        User = get_user_model()
        User.objects.all().delete()

    def create_colors(self):
        colors = [
            {"name": "Красный", "hex_code": "#FF0000"},
            {"name": "Синий", "hex_code": "#0000FF"},
            {"name": "Зеленый", "hex_code": "#00FF00"},
            {"name": "Черный", "hex_code": "#000000"},
            {"name": "Белый", "hex_code": "#FFFFFF"},
            {"name": "Дуб", "hex_code": "#C19A6B"},
            {"name": "Орех", "hex_code": "#773F1A"},
            {"name": "Серый", "hex_code": "#808080"},
            {"name": "Бежевый", "hex_code": "#F5F5DC"},
            {"name": "Коричневый", "hex_code": "#A52A2A"},
        ]

        color_objs = []
        for color_data in colors:
            slug = generate_unique_slug(Color, color_data['name'])
            color = Color.objects.create(
                name=color_data['name'],
                hex_code=color_data['hex_code'],
                slug=slug
            )
            color_objs.append(color)
            self.stdout.write(f'Created color: {color.name}')

        return color_objs

    def create_users(self):
        User = get_user_model()
        users = []
        for i in range(1, 11):
            user = User.objects.create_user(
                email=f'user{i}@example.com',
                password='password123',
                first_name=f'User{i}FirstName',
                last_name=f'User{i}LastName',
                phone=f'+123456789{i:02d}'
            )
            users.append(user)
            self.stdout.write(f'Created user: {user.email}')

        # Создаем администратора
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        users.append(admin)
        self.stdout.write(f'Created admin user: {admin.email}')

        # Создаем профили
        for user in users:
            # Проверяем, есть ли уже профиль
            if not hasattr(user, 'profile'):
                profile = Profile.objects.create(
                    user=user,
                    birth_date=datetime.now() - timedelta(days=random.randint(7000, 20000))
                )
                self.stdout.write(f'Created profile for {user.email}')

        return users

    def create_categories(self):
        categories = []
        category_names = ["Диваны", "Кресла", "Столы", "Стулья", "Кровати", "Шкафы", "Комоды", "Тумбы", "Стеллажи",
                          "Пуфы"]
        for name in category_names:
            slug = generate_unique_slug(Category, name)
            category = Category.objects.create(
                name=name,
                slug=slug,
                description=lorem.paragraph(),
                is_featured=random.choice([True, False])  # Добавляем случайный флаг
            )

            # Добавляем изображение для категории
            image = create_dummy_image(text=f"Category {name}")
            category.image.save(image.name, image, save=True)

            categories.append(category)
            self.stdout.write(f'Created category: {name} with slug {slug}')

        return categories

    def create_collections(self):
        collections = []
        collection_names = ["Классика", "Модерн", "Лофт", "Скандинавский", "Прованс", "Минимализм", "Ар-деко", "Эко"]
        for name in collection_names:
            slug = generate_unique_slug(Collection, name)
            collection = Collection.objects.create(
                name=name,
                slug=slug,
                description=lorem.paragraph(),
                is_featured=random.choice([True, False])
            )

            # Добавляем изображение для коллекции
            image = create_dummy_image(text=f"Collection {name}")
            collection.image.save(image.name, image, save=True)

            collections.append(collection)
            self.stdout.write(f'Created collection: {name} with slug {slug}')

        return collections

    def create_products(self, categories, collections, colors):
        products = []
        for i in range(1, 51):
            name = f'Товар {i}'
            slug = generate_unique_slug(Product, name)
            product = Product.objects.create(
                name=name,
                slug=slug,
                description=lorem.paragraph(),
                category=random.choice(categories),
                base_price=Decimal(random.randint(5000, 50000) / 100)
            )

            # Добавляем коллекции
            product.collections.set(random.sample(collections, k=random.randint(1, 3)))

            # Добавляем главное изображение
            main_image = create_dummy_image(text=f"Main {name}")
            product.main_image.save(main_image.name, main_image, save=True)

            # Добавляем дополнительные изображения товара
            for img_idx in range(1, random.randint(2, 5)):
                image = create_dummy_image(text=f"Product {i} Image {img_idx}")
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    alt_text=f"Изображение {img_idx} для {name}",
                    order=img_idx
                )

            # Создаем варианты для каждого товара
            variants_count = random.randint(2, 5)
            for j in range(1, variants_count + 1):
                is_default = (j == 1)  # Первый вариант делаем по умолчанию
                color = random.choice(colors)

                variant = ProductVariant.objects.create(
                    product=product,
                    color=color,
                    size=random.choice(["S", "M", "L", "XL", ""]),
                    material=random.choice(["Дерево", "Металл", "Ткань", "Кожа", "Пластик", "Стекло"]),
                    sku=f'PRD-{i}-VAR-{j}',
                    price_modifier=Decimal(random.randint(-500, 500) / 100),
                    stock=random.randint(0, 20),
                    is_default=is_default
                )

                # Добавляем изображения для варианта
                for img_idx in range(1, random.randint(1, 4)):
                    try:
                        # Преобразуем HEX в RGB
                        hex_color = color.hex_code.lstrip('#')
                        rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
                    except:
                        rgb_color = (200, 200, 200)

                    image = create_dummy_image(
                        color=rgb_color,
                        text=f"Variant {j} Image {img_idx}"
                    )
                    VariantImage.objects.create(
                        variant=variant,
                        image=image,
                        alt_text=f"Изображение {img_idx} для варианта {color.name}",
                        order=img_idx
                    )

            products.append(product)
            self.stdout.write(f'Created product: {product.name} with slug {slug} and {variants_count} variants')

        return products

    def create_tags(self):
        tags = []
        tag_names = ["Дизайн", "Интерьер", "Советы", "Тренды", "Новинки", "Акции", "Стиль", "Декор"]
        for name in tag_names:
            slug = generate_unique_slug(Tag, name)
            tag = Tag.objects.create(name=name, slug=slug)
            tags.append(tag)
            self.stdout.write(f'Created tag: {name} with slug {slug}')

        return tags

    def create_blog_posts(self, users, tags):
        for i in range(1, 21):
            title = f'Пост {i}: {lorem.sentence()}'
            slug = generate_unique_slug(Post, title)
            post = Post.objects.create(
                title=title,
                slug=slug,
                content=lorem.paragraph() * 5,
                author=random.choice(users),
                is_published=random.choice([True, False])
            )

            # Добавляем изображение для поста
            image = create_dummy_image(text=f"Post {i}")
            post.image.save(image.name, image, save=True)

            post.tags.set(random.sample(tags, k=random.randint(1, 4)))
            self.stdout.write(f'Created post: {title} with slug {slug}')

    def create_reviews(self, products, users):
        for product in random.sample(products, k=30):
            for user in random.sample(users, k=random.randint(1, 5)):
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=random.randint(1, 5),
                    title=f'Отзыв на {product.name}',
                    text=lorem.paragraph(),
                    is_approved=random.choice([True, False])
                )

    def create_carts(self, users):
        for user in users:
            cart, created = Cart.objects.get_or_create(user=user)
            if created:
                # Получаем все варианты товаров
                all_variants = list(ProductVariant.objects.all())

                # Выбираем уникальные варианты для этой корзины
                selected_variants = set()
                for _ in range(random.randint(0, 5)):
                    # Если варианты закончились, выходим из цикла
                    if not all_variants:
                        break

                    # Выбираем случайный вариант и удаляем его из списка
                    variant = random.choice(all_variants)
                    all_variants.remove(variant)
                    selected_variants.add(variant)

                    # Создаем элемент корзины
                    CartItem.objects.create(
                        cart=cart,
                        variant=variant,
                        quantity=random.randint(1, 3)
                    )

    def create_orders(self, users):
        statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        for i in range(1, 31):
            user = random.choice(users)
            order = Order.objects.create(
                user=user,
                status=random.choice(statuses),
                total=Decimal(0),
                address=f'Адрес доставки {i}',
                phone=user.phone,
                email=user.email,
                comment=lorem.sentence()
            )

            # Создаем элементы заказа
            total = Decimal(0)
            for _ in range(random.randint(1, 5)):
                variant = random.choice(ProductVariant.objects.all())
                quantity = random.randint(1, 3)
                price = variant.price

                # ИСПРАВЛЕНИЕ: Добавляем product=variant.product
                OrderItem.objects.create(
                    order=order,
                    variant=variant,
                    product=variant.product,  # <-- Добавлено это поле
                    quantity=quantity,
                    price=price,
                    name=variant.product.name,
                    sku=variant.sku
                )
                total += price * quantity

            order.total = total
            order.save()

    def add_favorites(self, users, products):
        for user in users:
            # Убедимся, что у пользователя есть профиль
            if hasattr(user, 'profile'):
                favorites = random.sample(products, k=random.randint(0, 10))
                user.profile.favorites.set(favorites)