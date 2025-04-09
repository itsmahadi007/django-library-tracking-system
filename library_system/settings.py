import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
running_in_docker = os.environ.get("DJANGO_RUNNING_IN_DOCKER", "False")

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
DEBUG = int(os.getenv('DEBUG', default=1))
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost').split(' ')

# Applications
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'corsheaders',
    # Local apps
    'library',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'library_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add template directories if needed
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'library_system.wsgi.application'

if running_in_docker == "False":
    # print("Using local DB")
    # Database settings
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "django_tracking"
    DB_USER = "postgres"
    DB_PASSWORD = "1516"
    # Redis settings
    REDIS_HOST = "localhost"
    REDIS_PORT = "6379"
else:
    # Database settings
    # print("Running on Docker")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    # Redis settings
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # Add more validators as needed
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Celery Configuration
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'admin@library.com')

# Celery Beat
from .celery import app as celery_app

CELERY_TIMEZONE = 'UTC'

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'check_overdue_loans': {
        'task': 'library.tasks.check_overdue_loans',
        'schedule': crontab(hour=0, minute=0),
    },
}
