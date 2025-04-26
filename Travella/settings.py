from pathlib import Path
import os
from datetime import timedelta
from decouple import config

# Base directory path for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = 'django-insecure-y4()m#%)dc!1%*vmk)0m$lb9*@ybha2%o&(7b3jk8x7w*^@k)*'  # Keep secret in production
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['*']  # Specify hosts in production

# reCAPTCHA settings
RECAPTCHA_SITE_KEY = config("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = config("RECAPTCHA_SECRET_KEY")  # Needed for backend verification

# Installed applications
INSTALLED_APPS = [
    # Django core apps
    'daphne',  # ASGI support
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third-party apps
    'corsheaders',  # Cross-Origin Resource Sharing
    'rest_framework_simplejwt',  # JWT authentication
    'rest_framework',  # REST API framework
    'channels',  # WebSocket support
    'django_extensions',  # Development utilities
    # Local project apps
    'apps.utils',
    'apps.accounts',
    'apps.dashboard',
    'apps.security',
    'apps.users',
    'apps.appinstallations',
    'apps.reports',
    'apps.masterentry',
    'apps.guides'
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS handling
    'django.middleware.common.CommonMiddleware',  # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Messaging framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# URL configuration
ROOT_URLCONF = 'Travella.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Custom template directory
        'APP_DIRS': True,  # Enable app template directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.accounts.context_processors.recaptcha_context',
            ],
        },
    },
]

# Application definitions
WSGI_APPLICATION = 'Travella.wsgi.application'  # WSGI entry point
ASGI_APPLICATION = 'Travella.asgi.application'  # ASGI entry point

# Channel layers for WebSocket support
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',  # Use Redis in production
    },
}

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT auth
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.MultiPartParser',  # File uploads
        'rest_framework.parsers.FormParser',  # Form data
        'rest_framework.parsers.JSONParser',  # JSON data
    ),
}

# Password validation rules
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True  # Enable timezone support

# Static and media file settings
STATIC_URL = '/static/'  # URL prefix for static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Static files directory
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Add this
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Whitenoise

MEDIA_URL = '/media/'  # URL prefix for media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Media files directory

# Database settings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default primary key type
AUTH_USER_MODEL = 'accounts.User'  # Custom user model

# JWT configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=480),  # 8 hours
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 1 day
    "AUTH_HEADER_TYPES": ("Bearer",),  # Authorization header type
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",  # JWT ID claim
}

# CORS headers configuration
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Accoundid',
    'Authorizationheader',
    'Sessiontoken',
]

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'testing@singledeck.in'
EMAIL_HOST_PASSWORD = 'Nimai1234$'
DEFAULT_FROM_EMAIL = 'testing@singledeck.in'

# SMS configuration
TXTLCL_BASE_URL = "https://api.textlocal.in/send/"  # Textlocal API endpoint

# Frame options
X_FRAME_OPTIONS = 'ALLOW-FROM https://swc.singledeck.in/'  # Allow embedding from specific domain

# Logging configuration
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')  # Log directory
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)  # Create logs directory if it doesn't exist

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',  # Log errors and above
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {  # Django-specific logging
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'apps': {  # Application-specific logging
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Import additional configuration if available
try:
    from Travella.config import *  # Custom configuration override
except ImportError:
    pass  # Silently ignore if config file is missing
