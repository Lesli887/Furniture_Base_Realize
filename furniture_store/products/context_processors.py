from .models import Category, Collection
from cart.utils import get_cart_for_user
from users.models import Profile


def global_data(request):
    # Данные для хедера
    context = {
        'categories': Category.objects.all(),
        'featured_collections': Collection.objects.filter(is_featured=True)[:5],
    }

    # Данные для корзины
    cart = get_cart_for_user(request.user if request.user.is_authenticated else None)
    context['cart'] = cart

    # Данные для избранного
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            context['favorites_count'] = profile.favorites.count()
        except Profile.DoesNotExist:
            context['favorites_count'] = 0
    else:
        context['favorites_count'] = 0

    return context