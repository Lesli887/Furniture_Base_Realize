from .models import Cart

def get_cart_for_user(user):
    if user and user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    return None  # Для анонимных пользователей