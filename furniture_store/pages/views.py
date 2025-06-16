from django.views.generic import TemplateView
from products.models import Category, Collection, Product
from blog.models import Post
from django.db.models import Count

class StaticPageView(TemplateView):
    template_name = 'apps/pages/static_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Сопоставление URL-путей с заголовками страниц
        page_titles = {
            'delivery': 'Доставка и оплата',
            'guarantee': 'Гарантия',
            'assembly': 'Сборка мебели',
            'contacts': 'Контакты',
        }

        page_slug = self.kwargs.get('page_slug')
        context['page_title'] = page_titles.get(page_slug, page_slug.capitalize())
        return context


# Специальный view для главной страницы
class HomePageView(TemplateView):
    template_name = 'apps/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 4 популярные категории
        context['categories'] = Category.objects.annotate(
            product_count=Count('product')
        ).order_by('-product_count')[:4]

        # 3 избранные коллекции
        context['featured_collections'] = Collection.objects.filter(
            is_featured=True
        )[:3]

        # 4 популярных товара (по количеству заказов)
        context['popular_products'] = Product.objects.annotate(
            order_count=Count('order_items')
        ).order_by('-order_count')[:4]

        # 3 последние статьи блога
        context['latest_posts'] = Post.objects.filter(
            is_published=True
        ).order_by('-created_at')[:3]  # Изменено здесь

        return context