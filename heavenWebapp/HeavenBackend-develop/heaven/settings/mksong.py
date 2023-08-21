from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "heaven",
        "USER": "root",
        "PASSWORD": "digital23!",
        "HOST": "127.0.0.1",
        "PORT": "3307",
        "OPTIONS": {"init_command": 'SET sql_mode="STRICT_TRANS_TABLES"'},
    }
}
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
    # "EXCEPTION_HANDLER": "modules.exceptions.api_exception.custom_exception_handler",
}

APSCHEDULER_JOBSTORES = {
    "default": {
        "type": "sqlalchemy",
        "url": "mysql+pymysql://root:digital23!@localhost/heaven",
    }
}
TIME_ZONE = "Asia/Seoul"
USE_TZ = False
