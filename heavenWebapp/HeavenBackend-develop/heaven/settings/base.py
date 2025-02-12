"""
Django settings for heaven project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# from .logging_formatter import CustomFormatter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-nw3+$y=*8l2(8cd!j1hlp#=!-ryo9ddl=i5vr-k!ohbac)v#=e"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
LOGIN_REDIRECT_URL = "/"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",  # 세션 인증 클래스 유지
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",  # 모든 요청에 대해 허용
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",  # JSON 렌더링 사용
    ),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),  # JSON 파서 사용
    "DEFAULT_CSRF_COOKIE_NAME": "csrftoken",  # CSRF 토큰 쿠키 이름 설정
    "DEFAULT_CSRF_COOKIE_SECURE": False,  # CSRF 토큰 쿠키를 HTTPS로만 전송하지 않도록 설정
    "DEFAULT_CSRF_COOKIE_SAMESITE": None,  # 모든 요청에 대해 CSRF 토큰 쿠키 전송 허용
    "DEFAULT_AUTHENTICATION_CLASSES": [],  # CSRF 보호 비활성화
    "EXCEPTION_HANDLER": "modules.exceptions.api_exception.custom_exception_handler",
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": 10,  # 한 페이지에 표시할 아이템 수 설정
}

# Application definition
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,  # Optional: 세션 인증 사용 여부
    "SECURITY_DEFINITIONS": {},  # Optional: 보안 정의 설정
    "TAGS_SORTER": "alpha",
    "DOC_EXPANSION": "none",
}

AUTH_USER_MODEL = "accounts.User"
APPEND_SLASH = True
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.CommonCode",
    "corsheaders",
    "django_mysql",
    "apps.accounts",
    "rest_framework",
    "apps.groups",
    "apps.prm",
    "apps.HWCheck",
    "apps.virtualanalysis",
    "drf_yasg",
    "apps.HWSpec",
    "apps.measurement",
    "django_apscheduler",
    "apps.document",
    "reversion",
    "apps.webapp",
    "channels",
    "apps.testapp",  # test용 앱 배포시 삭제할 것
]
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "reversion.middleware.RevisionMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 요청 user logging 미들웨어
    "heaven.middleware.RequestUserLoggingMiddleware",
]

ROOT_URLCONF = "heaven.urls"

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

WSGI_APPLICATION = "heaven.wsgi.application"
ASGI_APPLICATION = "heaven.asgi.application"
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "formatters": {
        "simple": {"()": "heaven.logging_formatter.CustomFormatter"},
    },
}

ALLOWED_HOSTS = ["127.0.0.1", "54.180.186.50", "0.0.0.0"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8001"]
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = ["http://0.0.0.0", "https://0.0.0.0"]
CORS_ALLOW_CREDENTIALS = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "fkdlzldeja@gmail.com"
EMAIL_HOST_PASSWORD = "iadbfcrujbjhczal"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # 또는 Redis를 사용할 수 있음
    }
}
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",  # 또는 Redis를 사용할 수 있음
#         # "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",  # 또는 Redis를 사용할 수 있음
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     }
# }

WEBSOCKET_LOG_PATH = "./logs"
