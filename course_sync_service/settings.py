import os
from pathlib import Path
from datetime import timedelta

from course_sync_service.setting.paths import *
#from course_sync_service.setting.databases import DATABASES, DATABASE_ROUTERS
from course_sync_service.setting.logging import LOGGING
from course_sync_service.setting.apps import INSTALLED_APPS
from course_sync_service.setting.host import (
    ALLOWED_HOSTS,
    CSRF_TRUSTED_ORIGINS,
    CORS_ALLOWED_ORIGINS,
    CORS_ALLOW_ALL_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    SECURE_PROXY_SSL_HEADER
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


SECRET_KEY = os.getenv("SECRET_KEY", "false")
DEBUG = os.getenv("DJANGO_DEBUG", "False").strip().lower() == "true"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "course_sync_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "course_sync_service.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "es-es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Course Sync Service API',
    'DESCRIPTION': (
        "Course Sync Service API es un servicio que actúa como un puente de "
        "integración entre SINU y Google Classroom, permitiendo la creación, "
        "actualización y administración automatizada de cursos académicos. "
        "La API sincroniza información institucional como asignaturas, docentes, "
        "estudiantes y grupos, para generar aulas virtuales en Classroom de manera "
        "segura, consistente y sin intervención manual."
    ),
    'VERSION': '1.0.0',
}
