from pathlib import Path
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (если он существует)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# 1. АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ ОКРУЖЕНИЯ
# ==========================================
# По умолчанию считаем, что это локальная разработка ('local')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local').lower()
IS_DOCKER = (ENVIRONMENT == 'docker')

if IS_DOCKER:
    # Настройки для запуска внутри Docker-контейнера
    DEBUG = False
    ALLOWED_HOSTS = ['web', 'nginx', 'localhost', '127.0.0.1', '*']
    DEFAULT_DB_HOST = 'db'
else:
    # Настройки для локального запуска на компьютере
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    DEFAULT_DB_HOST = 'localhost'

# Если ключа нет в .env, используем заглушку, чтобы локально не падало
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-local-dev-key-change-me')

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost',
]

# Куки безопасны только если DEBUG = False (то есть в Docker/на продакшене)
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


# ==========================================
# 2. ПРИЛОЖЕНИЯ И MIDDLEWARE
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'main',
    'cart',
    'users',
    'orders',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'cart.middleware.CartMiddleware',
]

ROOT_URLCONF = 'kunteynir.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                'cart.context_processors.cart_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'kunteynir.wsgi.application'


# ==========================================
# 3. БАЗА ДАННЫХ
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'kunteynir_db'),
        'USER': os.getenv('POSTGRES_USER', 'kunteynir_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'kunteynir_password'),
        # УМНАЯ ЛОГИКА: берем из .env, а если там пусто — подставляем 'db' или 'localhost'
        'HOST': os.getenv('POSTGRES_HOST', DEFAULT_DB_HOST),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'ATOMIC_REQUESTS': True
    }
}


# ==========================================
# 4. ВАЛИДАЦИЯ ПАРОЛЕЙ И ИНТЕРНАЦИОНАЛИЗАЦИЯ
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'  # Рекомендую поменять на русский, раз сайт на русском
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_TZ = True


# ==========================================
# 5. СТАТИКА И МЕДИАФАЙЛЫ
# ==========================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Если у вас есть папка static с вашими исходными CSS/картинками, Django будет искать их здесь
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# 6. ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# ==========================================
SESSION_COOKIE_AGE = 2592000  # 30 дней (86400 секунд = 1 день, для 30 дней нужно 2592000)
SESSION_SAVE_EVERY_REQUEST = True

AUTH_USER_MODEL = 'users.CustomUser'

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'