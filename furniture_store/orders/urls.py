from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),

    # URL для оплаты онлайн
    path('payment/<int:order_id>/', views.payment_init, name='payment_init'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),

    # Новый URL для подтверждения заказа с оплатой при получении
    path('created/upon-receipt/<int:order_id>/', views.order_created_upon_receipt, name='order_created_upon_receipt'),
]