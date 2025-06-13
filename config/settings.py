from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-change-me"
DEBUG = True
ALLOWED_HOSTS = ["*"]
API_AUTH_TOKEN = "token-430"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "magasin",
    'rest_framework',
    'drf_yasg',
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware", 
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Entrez "Token token-430"',
        }
    }
}

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "lab3db"),
        "USER": os.getenv("POSTGRES_USER", "labuser"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "labpass"),
        "HOST": os.getenv("DB_HOST", "db-labo3"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "America/Toronto"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "magasin" / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOW_ALL_ORIGINS = True