
from datetime import timedelta
from pathlib import Path

# Importing os module to access environment variables
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Brings the secret key from the environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Brings the debug value from the environment variable


#
#
#
if os.environ.get('DEBUG') == '1':
    DEBUG = True
else:
    DEBUG = False
print(f"DEBUG Value in .env =============== {os.environ.get('DEBUG')}")
print(f"DEBUG Value in settings.py =============== {DEBUG}")
#
#
#



# Brings the allowed hosts from the environment variable
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')
print(f"Allowed Hosts ================= {ALLOWED_HOSTS}")

# Setting default usermodel to custo104.248.34.81
AUTH_USER_MODEL = 'useraccount.User'

# For allauth login
SITE_ID = 1

#
#
#
# Check if the application is running in debug mode
if DEBUG:
    # If in debug mode, set the website URL to the local development server
    WEBSITE_URL = 'http://localhost:8000'
else:
    # If not in debug mode (i.e., in production), set the website URL to the public IP address and port
    WEBSITE_URL = 'https://djangobnb.com'
print(f"WEBSITE_URL =================== {WEBSITE_URL}")
#
#
#

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://104.248.34.81:1337',
    'http://104.248.34.81:3000',
    'http://104.248.34.81',
    'https://djangobnb.com',
    'https://djangobnb.netlify.app',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://104.248.34.81:1337',
    'http://104.248.34.81:3000',
    'http://104.248.34.81',
    'https://djangobnb.com',
    'https://djangobnb.netlify.app',
]

# 
# Cors Settings
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'
CSRF_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'

# SIMEPLE_JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": "secret",
    "ALGORITHM": "HS512",
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Allauth settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# REST_FRAMEWORK settings for authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# REST_AUTH settings
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
}

# Channel Layers for Chat function
CHANNEL_LAYERS ={
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Application definition
INSTALLED_APPS = [
    'daphne',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    'allauth',
    'allauth.account',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    'corsheaders',

    # Custom
    'useraccount',
    'property',
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangobnb_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Entry point for http, https, etc into django
WSGI_APPLICATION = 'djangobnb_backend.wsgi.application'
# Entry point for websockets into django
ASGI_APPLICATION = 'djangobnb_backend.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# Print statements to verify environment variables
print(f"SQL_ENGINE: {os.environ.get('SQL_ENGINE')}")
print(f"SQL_DATABASE: {os.environ.get('SQL_DATABASE')}")
print(f"SQL_USER: {os.environ.get('SQL_USER')}")
print(f"SQL_PASSWORD: {os.environ.get('SQL_PASSWORD')}")
print(f"SQL_HOST: {os.environ.get('SQL_HOST')}")
print(f"SQL_PORT: {os.environ.get('SQL_PORT')}")
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
# Media files Setup
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
