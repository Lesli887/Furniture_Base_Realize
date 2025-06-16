import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "management"))

SECRET_KEY = 'django-insecure-+3#b(0!b5^g&v$e8r4%9s0k!j2n$#f7a6d*!@zxc'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',
    'crispy_bootstrap5',
    'django_bootstrap5',

    'core',
    'products',
    'cart',
    'orders',
    'users',
    'blog',
    'reviews',
    'pages',

    'image_uploader_widget',
    'ckeditor',
]

CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACK = 'bootstrap5'


STRIPE_PUBLISHABLE_KEY = 'pk_test_51RYyX5DGKCeV66Ei4A6uY4ESL94zoqmwUT0C2fcJa1zxr74NqQHUFBUyIyh8xYSA8g5dQUe0JS3HWxT1LYAgDE5Y00szQe8WgE'  # Замените на реальный ключ
STRIPE_CURRENCY = 'rub'  # Валюта: российский рубль

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'furniture_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'products.context_processors.global_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'furniture_store.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/users/login/'

ALLOWED_HTML_TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'strong', 'em', 'u', 's', 'span',
    'ul', 'ol', 'li', 'a', 'img', 'blockquote',
    'hr',  # Добавьте этот тег
    'div', 'table', 'tr', 'td', 'th',  # При необходимости
]

ALLOWED_HTML_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height', 'style', 'class'],
    '*': ['class', 'style'],  # Разрешить для всех элементов
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Styles'],
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Image', 'Blockquote'],
            ['RemoveFormat', 'Source']
        ],
        'contentsCss': '/static/css/apps/blog/ckeditor_content.css',
    }
}