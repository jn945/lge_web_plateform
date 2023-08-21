from drf_yasg import openapi
from rest_framework import serializers


class DocumentParam:
    get_pdf = [
        openapi.Parameter(
            "id_list",
            openapi.IN_QUERY,
            description="product specification id list를 넣어주세요",
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "export_type",
            openapi.IN_QUERY,
            description="선택된 export type을 넣어주세요.",
            type=openapi.TYPE_STRING,
        ),
    ]
