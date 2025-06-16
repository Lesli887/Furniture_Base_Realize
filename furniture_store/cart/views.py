from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import ProductVariant
from django.contrib import messages


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('variant__product').all()
    total = cart.total_price  # Используем новое свойство модели
    return render(request, 'apps/cart/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })


@login_required
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Проверка наличия на складе
    if variant.stock <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Товара нет в наличии'
            })
        messages.error(request, 'Товара нет в наличии')
        return redirect('products:product_detail', slug=variant.product.slug)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Товар {variant.product.name} добавлен в корзину',
            'cart_item_count': cart.item_count
        })
    else:
        messages.success(request, f'Товар {variant.product.name} добавлен в корзину')
        return redirect('cart:cart_view')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Товар удален из корзины')
    return redirect('cart:cart_view')


@login_required
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    # Проверка наличия на складе
    if quantity > cart_item.variant.stock:
        messages.error(request, f'Недостаточно товара на складе. Доступно: {cart_item.variant.stock} шт.')
        return redirect('cart:cart_view')

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart_view')