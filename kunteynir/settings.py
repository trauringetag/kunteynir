from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


ENVIRONMENT = os.getenv('ENVIRONMENT', 'local').lower()
IS_DOCKER = (ENVIRONMENT == 'docker')


if IS_DOCKER:
    DEBUG = True
    ALLOWED_HOSTS = ['web', 'nginx', 'localhost', '127.0.0.1', '*']
    DEFAULT_DB_HOST = 'db'
else:
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    DEFAULT_DB_HOST = 'localhost'


SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-local-dev-key-change-me')


CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost',
]


CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


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
                'django.template.context_processors.media',
            ],
        },
    },
]


WSGI_APPLICATION = 'kunteynir.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'kunteynir_db'),
        'USER': os.getenv('POSTGRES_USER', 'kunteynir_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'kunteynir_password'),
        'HOST': os.getenv('POSTGRES_HOST', DEFAULT_DB_HOST),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'ATOMIC_REQUESTS': True
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'


USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


SESSION_COOKIE_AGE = 2592000
SESSION_SAVE_EVERY_REQUEST = True


AUTH_USER_MODEL = 'users.CustomUser'


STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'