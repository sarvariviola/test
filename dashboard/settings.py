"""
Django beállítások a statisztikai elemzési platformhoz.
Készítette: Sárvári Viola
"""

from pathlib import Path
import environ
import os

# A projekt gyökérkönyvtárának meghatározása
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()

# Biztonsági beállítások
# FIGYELEM: Production környezetben cseréld le ezt a secret key-t és állítsd DEBUG = False-ra
SECRET_KEY = 'django-insecure-baf@%%!z%qq8y4%%o(-o31ccw50i8si8wy4%x+uj9mv60&jt&9'

# Debug mód - csak fejlesztéshez, production-ben mindig False legyen
DEBUG = True

ALLOWED_HOSTS = ["*","185.51.188.182","viola.quic.hu",]

# Telepített Django alkalmazások
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

ROOT_URLCONF = 'dashboard.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'dashboard.wsgi.application'

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media/')

# Adatbázis konfiguráció
# A kapcsolódási adatok a .env fájlból kerülnek beolvasásra
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Jelszó validációs szabályok
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

# Nemzetköziesítési beállítások
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Statikus fájlok kezelése (CSS, JavaScript, képek)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Alapértelmezett elsődleges kulcs mező típusa
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
