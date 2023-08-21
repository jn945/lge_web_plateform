from collections import OrderedDict

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from modules.common.params import CommonParams
from modules.common.utils import default_response
from modules.common.viewset import CustomViewset
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import VirtualAnalysisRequest,CAEData
from .serializers import VirtualAnalysisRequestSerializer,CAEDataSerializer

# Create your views here.


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return default_response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            ),
            status=status.HTTP_200_OK,
        )

    page_query_param = "page"
    page_query_description = "page num을 입력해주세요"
    page_size_query_param = "page_size"
    page_size_query_description = "page size 을 입력해주세요"

    page_size = 20  # 한 페이지에 표시할 아이템 수 설정


class VirtualAnalysisRequestViewSet(CustomViewset):
    queryset = VirtualAnalysisRequest.objects.all()
    serializer_class = VirtualAnalysisRequestSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"],
        manual_parameters=CommonParams.list_get_params,
        peration_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # bulk create 생성 -> list 로 받아서 처리합니다.
    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"],
        manual_parameters=CommonParams.merge,
        operation_description="설명입니다",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        # return Response("done")

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"], operation_description="설명입니다"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"], operation_description="설명입니다"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"], operation_description="설명입니다"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"], operation_description="설명입니다"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class CAEDataViewSet(CustomViewset):
    queryset = CAEData.objects.all()
    serializer_class = CAEDataSerializer

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"],
        manual_parameters=CommonParams.list_get_params,
        peration_description="설명입니다",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # bulk create 생성 -> list 로 받아서 처리합니다.
    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"],
        manual_parameters=CommonParams.merge,
        operation_description="설명입니다",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        # return Response("done")

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"], operation_description="설명입니다"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"], operation_description="설명입니다"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"], operation_description="설명입니다"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["[Virtual Analysis] Request"], operation_description="설명입니다"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    


