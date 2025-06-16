from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    # Коллекции
    path('collections/', views.collection_list, name='collection_list'),
    path('collection/<slug:slug>/', views.collection_detail, name='collection_detail'),
]