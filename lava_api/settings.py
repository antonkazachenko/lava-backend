from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'a-simple-secret-key-that-does-not-need-to-be-hidden'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Applications
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'apiapp',
    "corsheaders",
]

# REST framework config: JSON only, no auth
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],  # no auth
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'UNAUTHENTICATED_USER': None,
}

# Middleware, with WhiteNoise for static file serving
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

# Dummy DB (we load from CSV instead)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# Skip migrations for apiapp
MIGRATION_MODULES = {
    'apiapp': None,
}

ROOT_URLCONF = 'lava_api.urls'

# Minimal template setup (none required for JSON-only API)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {},
    },
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://lava-data-lamp.netlify.app"
]

WSGI_APPLICATION = 'lava_api.wsgi.application'

# Static files (with WhiteNoise)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
