from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import stripe

from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .forms import OrderForm

# Настройка Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('variant').all()

    # Проверка наличия товаров
    for item in cart_items:
        if item.quantity > item.variant.stock:
            messages.error(
                request,
                f'Недостаточно товара "{item.variant.product.name}" на складе. Доступно: {item.variant.stock} шт.'
            )
            return redirect('cart:cart_view')

    if not cart_items:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart:cart_view')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = sum(item.total_price for item in cart_items)
            order.save()

            # Создаем позиции заказа
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    variant=cart_item.variant,
                    product=cart_item.variant.product,
                    quantity=cart_item.quantity,
                    price=cart_item.variant.price,
                    name=cart_item.variant.product.name,
                    sku=cart_item.variant.sku
                )
                # Уменьшаем количество товара на складе
                cart_item.variant.stock -= cart_item.quantity
                cart_item.variant.save()

            # Очищаем корзину
            cart_items.delete()

            # Перенаправляем на страницу оплаты
            return redirect('orders:payment_init', order_id=order.id)
    else:
        form = OrderForm(initial={
            'email': request.user.email,
            'phone': request.user.phone,
        })

    total = sum(item.total_price for item in cart_items)
    return render(request, 'apps/orders/order_create.html', {
        'form': form,
        'cart': cart,
        'total': total
    })


@login_required
def payment_init(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    success_url = request.build_absolute_uri(
        reverse('orders:payment_success', args=[order.id])  # Добавить order_id
    )
    cancel_url = request.build_absolute_uri(
        reverse('orders:payment_cancel')
    )

    session_data = {
        'mode': 'payment',
        'client_reference_id': order.id,
        'success_url': success_url,
        'cancel_url': cancel_url,
        'line_items': []
    }

    # Добавляем товары в сессию Stripe
    for item in order.items.all():
        session_data['line_items'].append({
            'price_data': {
                'currency': settings.STRIPE_CURRENCY,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),  # в копейках
            },
            'quantity': item.quantity,
        })

    # Создаем сессию Stripe
    try:
        session = stripe.checkout.Session.create(**session_data)
        order.stripe_id = session.id
        order.save()
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f'Ошибка при создании платежа: {str(e)}')
        return redirect('orders:order_detail', order_id=order.id)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.payment_status = 'paid'
    order.save()
    messages.success(request, 'Оплата прошла успешно!')
    return render(request, 'apps/orders/order_created.html', {'order': order})


@login_required
def payment_cancel(request):
    messages.warning(request, 'Оплата была отменена')
    return redirect('orders:order_list')


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'apps/orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'apps/orders/order_detail.html', {'order': order})