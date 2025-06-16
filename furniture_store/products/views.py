from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.shortcuts import render, get_object_or_404
import re

from cart.models import Cart
from reviews.models import Review
from .models import Product, Category, Collection, ProductVariant

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404

from cart.models import Cart
from reviews.models import Review
from .models import Product, Category, Collection, ProductVariant


def product_list(request):
    # Получаем параметры фильтрации из GET-запроса
    search_query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category')
    collection_slug = request.GET.get('collection')
    sort_by = request.GET.get('sort', 'newest')
    stock_filter = request.GET.get('stock', 'all')
    page_number = request.GET.get('page', 1)
    featured_collections = Collection.objects.filter(is_featured=True)[:5]

    # Начальный набор товаров
    products = Product.objects.all().prefetch_related('variants', 'images', 'collections')

    # Применяем фильтры
    if search_query:
        # Экранируем специальные символы для regex
        pattern = re.escape(search_query)
        products = products.filter(
            Q(name__iregex=pattern) |
            Q(category__name__iregex=pattern) |
            Q(collections__name__iregex=pattern)
        ).distinct()

    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)

    if collection_slug and collection_slug != 'all':
        products = products.filter(collections__slug=collection_slug)

    if stock_filter == 'in-stock':
        products = products.filter(variants__stock__gt=0).distinct()

    # Применяем сортировку
    if sort_by == 'price-low':
        products = products.order_by('base_price')
    elif sort_by == 'price-high':
        products = products.order_by('-base_price')
    elif sort_by == 'popular':
        products = products.annotate(
            order_count=Count('order_items')
        ).order_by('-order_count')
    elif sort_by == 'rating':
        products = products.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating')
    else:  # 'newest'
        products = products.order_by('-created_at')

    # Пагинация
    paginator = Paginator(products, 12)  # 12 товаров на странице
    page_obj = paginator.get_page(page_number)

    # Контекст для шаблона
    context = {
        'products': page_obj,
        'categories': Category.objects.all(),
        'collections': Collection.objects.all(),
        'current_category': category_slug,
        'current_collection': collection_slug,
        'current_sort': sort_by,
        'current_stock': stock_filter,
        'page_obj': page_obj,
        'featured_collections': featured_collections,
        'search_query': search_query,
    }

    return render(request, 'apps/products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.all()

    # Инициализируем cart как None для анонимных пользователей
    cart = None

    # Получаем корзину только для авторизованных пользователей
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

    # Получаем только одобренные отзывы
    approved_reviews = Review.objects.filter(
        product=product,
        is_approved=True
    ).order_by('-created_at')

    # Последние 3 отзыва для предпросмотра
    preview_reviews = approved_reviews[:3]

    # Проверяем, есть ли отзыв от текущего пользователя
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            product=product,
            user=request.user
        ).first()

    return render(request, 'apps/products/product_detail.html', {
        'product': product,
        'variants': variants,
        'cart': cart,  # Может быть None для анонимных пользователей
        'preview_reviews': preview_reviews,
        'reviews_count': approved_reviews.count(),
        'user_review': user_review
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    # Получаем параметры фильтрации
    collection_slug = request.GET.get('collection')
    sort_by = request.GET.get('sort', 'newest')
    stock_filter = request.GET.get('stock', 'all')
    page_number = request.GET.get('page', 1)

    # Начальный набор товаров
    products = Product.objects.filter(category=category).prefetch_related('variants', 'images', 'collections')

    # Применяем фильтры
    if collection_slug and collection_slug != 'all':
        products = products.filter(collections__slug=collection_slug)

    if stock_filter == 'in-stock':
        products = products.filter(variants__stock__gt=0).distinct()

    # Применяем сортировку
    if sort_by == 'price-low':
        products = products.order_by('base_price')
    elif sort_by == 'price-high':
        products = products.order_by('-base_price')
    elif sort_by == 'popular':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.order_by('-created_at')
    else:  # 'newest'
        products = products.order_by('-created_at')

    # Пагинация
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)

    # Контекст для шаблона
    context = {
        'category': category,
        'products': page_obj,
        'collections': Collection.objects.all(),
        'current_collection': collection_slug,
        'current_sort': sort_by,
        'current_stock': stock_filter,
        'page_obj': page_obj,
    }

    return render(request, 'apps/products/category_detail.html', context)


def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug)

    # Получаем параметры фильтрации
    category_slug = request.GET.get('category', 'all')
    sort_by = request.GET.get('sort', 'newest')
    stock_filter = request.GET.get('stock', 'all')
    page_number = request.GET.get('page', 1)

    # Начальный набор товаров
    products = Product.objects.filter(collections=collection).prefetch_related('variants', 'images')

    # Применяем фильтры
    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)

    if stock_filter == 'in-stock':
        products = products.filter(variants__stock__gt=0).distinct()

    # Применяем сортировку
    if sort_by == 'price-low':
        products = products.order_by('base_price')
    elif sort_by == 'price-high':
        products = products.order_by('-base_price')
    elif sort_by == 'popular':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.order_by('-created_at')
    else:  # 'newest'
        products = products.order_by('-created_at')

    # Пагинация
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)

    # Контекст для шаблона
    context = {
        'collection': collection,
        'products': page_obj,
        'categories': Category.objects.all(),
        'current_category': category_slug,  # Добавлено для сохранения состояния
        'current_sort': sort_by,  # Добавлено для сохранения состояния
        'current_stock': stock_filter,  # Добавлено для сохранения состояния
        'page_obj': page_obj,
    }

    return render(request, 'apps/products/collection_detail.html', context)

def collection_list(request):
    collections = Collection.objects.all()
    context = {
        'collections': collections,
        'title': 'Все коллекции',
    }
    return render(request, 'apps/products/collection_list.html', context)