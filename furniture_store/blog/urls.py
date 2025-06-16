from django.urls import path
from . import views

app_name = 'blog'  # Важно: определить app_name

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
]