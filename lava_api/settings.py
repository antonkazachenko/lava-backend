# lava_api/settings.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'a-simple-secret-key-that-does-not-need-to-be-hidden'
DEBUG = False
ALLOWED_HOSTS = ['*']

# Minimal apps needed for a simple API
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'rest_framework',
    'apiapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- ADD THIS LINE
]

ROOT_URLCONF = 'lava_api.urls'
TEMPLATES = []
WSGI_APPLICATION = 'lava_api.wsgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # <-- ADD THIS LINE