from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ProfileForm, UserForm
from .models import Profile
from orders.models import Order, OrderItem  # Добавляем импорт для работы с заказами
from reviews.models import Review  # Добавляем импорт для работы с отзывами


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('products:product_list')
    else:
        form = RegistrationForm()
    return render(request, 'apps/users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('products:product_list')
    else:
        form = LoginForm()
    return render(request, 'apps/users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('products:product_list')


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    favorites = profile.favorites.all()

    # Оптимизация запросов для заказов и отзывов
    latest_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5] \
        .prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related('product'),
            to_attr='prefetched_items'
        )
    )

    latest_reviews = Review.objects.filter(user=request.user).select_related('product')[:5]

    orders_count = Order.objects.filter(user=request.user).count()
    reviews_count = Review.objects.filter(user=request.user).count()

    return render(request, 'apps/users/profile.html', {
        'profile': profile,
        'favorites': favorites,
        'orders_count': orders_count,
        'reviews_count': reviews_count,
        'latest_orders': latest_orders,
        'latest_reviews': latest_reviews
    })


@login_required
def profile_edit(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('users:profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'apps/users/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def toggle_favorite(request, product_id):
    from products.models import Product
    product = Product.objects.get(id=product_id)
    profile = request.user.profile

    if product in profile.favorites.all():
        profile.favorites.remove(product)
        message = 'Товар удален из избранного'
        is_favorite = False
    else:
        profile.favorites.add(product)
        message = 'Товар добавлен в избранное'
        is_favorite = True

    # Получаем обновленное количество избранных товаров
    favorites_count = profile.favorites.count()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite,
            'message': message,
            'favorites_count': favorites_count
        })
    else:
        messages.info(request, message)
        return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))