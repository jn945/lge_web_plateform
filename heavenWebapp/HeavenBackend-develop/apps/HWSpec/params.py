from drf_yasg import openapi
from rest_framework import serializers


class HWSpecParams:
    categoty = [
        openapi.Parameter(
            "category",
            openapi.IN_QUERY,
            description="카테고리 입니다",
            type=openapi.TYPE_STRING,
            required=True,  # 필수 값으로 설정
        )
    ]
