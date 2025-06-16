from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('<str:page_slug>/', views.StaticPageView.as_view(), name='static_page'),
]