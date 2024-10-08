"""
Django settings for entag project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import gettext as _
from kombu.serialization import registry

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = BASE_DIR / "entagstatic"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-@68&po=$xem0nz1e(b)=38pdixp2k6_6cebbt!qaye_lec(!oa",
)

PUBLIC_KEY = config(
    "PUBLIC_KEY",
    default="django-bad_guy-bajebaje-@68&po=$xem0nz198gbygiosnioh$%^&*vnw0395e8u4tbvp2k6_6cebbt!qaye_lec(!oa",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # my apps
    "core",
    "accounts",
    "customer",
    "admin_dashboard",
    "payments",
    "website",
    # third party apps
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "corsheaders",
    "django_filters",
    "simple_history",
    # "storages",
    "cloudinary",
    "cloudinary_storage",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.google",
    # "django_extensions",
    # "django_celery_beat",
    # "django_celery_results",
    # "django_celery_beat.apps.CeleryConfig",
    # "django_celery_results.apps.CeleryConfig",
    # "django_celery_beat.apps.PeriodicTasksConfig",
    # "django_celery_results.apps.PeriodicTasksConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "entag.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


WSGI_APPLICATION = "entag.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    # settings.py
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": (
            config("INTERNAL_DB_URL")
            if config("DEPLOYMENT_RENDER", cast=bool)
            else config("EXTERNAL_DB_URL")
        ),
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "accounts.User"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

USE_I18N = True

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
    # Add more languages here
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "DOC_EXPANSION": "none",
}

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "core.exceptions.permission_exception_handler",
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_PAGINATION_CLASS": "core.pagination.StandardResultSetPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

WEB_TOKEN_EXPIRY = config("WEB_TOKEN_EXPIRY", cast=int)
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

CELERY_ENABLED = config("CELERY_ENABLED", default=False, cast=bool)
CELERY_BROKER_URL = config("CELERY_BROKER", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = config("CELERY_BROKER", "redis://localhost:6379/0")

# Optional: allauth settings
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"

CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json", "application/text", "application/json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
CELERY_TASK_TRACK_STARTED = True
CELERY_ACKS_LATE = True


registry.enable("json")
registry.enable("application/text")
registry.enable("application/json")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = config("STATIC_URL", "/static/")
STATIC_ROOT = PROJECT_ROOT / "staticfiles"

SITE_ID = 1

AWS_ACCESS_KEY_ID = "your-access-key"
AWS_SECRET_ACCESS_KEY = "your-secret-key"
AWS_STORAGE_BUCKET_NAME = "your-bucket-name"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_DEFAULT_ACL = "public-read"
AWS_LOCATION = "static"


CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:6100",
    "https://waitlist-khaki.vercel.app/",
    "https://backend-yxi1.onrender.com/swagger/",
]


CORS_ALLOW_ALL_ORIGINS = True
FRONTEND_ADMIN_URL = config("FRONTEND_ADMIN_URL")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
