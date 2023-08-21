from drf_yasg import openapi
from rest_framework import serializers


class PlanGroupParams:
    get = [
        openapi.Parameter(
            "plan_type",
            openapi.IN_QUERY,
            description="plan_type 입니다",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ]
    duplication = [
        openapi.Parameter(
            "group_name",
            openapi.IN_QUERY,
            description="group_name 넣어주세요",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ]


class PlanSeriesParams:
    list = [
        openapi.Parameter(
            "plan_type",
            openapi.IN_QUERY,
            description="plan_type 입니다",
            type=openapi.TYPE_STRING,
        ),
    ]


class PlanInfoParams:
    list = [
        openapi.Parameter(
            "column_name",
            openapi.IN_QUERY,
            description="column_name 입니다",
            type=openapi.TYPE_STRING,
        ),
    ]
