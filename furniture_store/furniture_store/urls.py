from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from pages.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),  # Главная страница
    path('pages/', include('pages.urls')),  # Статические страницы
    path('catalog/', include('products.urls')),  # Каталог товаров
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),
    path('blog/', include('blog.urls')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)