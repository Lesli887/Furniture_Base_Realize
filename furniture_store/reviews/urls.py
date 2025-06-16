from django.urls import path
from . import views

app_name = 'product_reviews'  # Изменено на уникальное имя

urlpatterns = [
    path('add/<int:product_id>/', views.add_review, name='add_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('product/<int:product_id>/', views.product_reviews, name='product_reviews'),
]