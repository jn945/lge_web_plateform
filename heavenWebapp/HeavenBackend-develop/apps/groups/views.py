from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from modules.common.viewset import CustomViewset
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CustomGroup
from .serializers import GroupSerializer


class GroupViewSet(CustomViewset):
    queryset = CustomGroup.objects.all()
    serializer_class = GroupSerializer

    @swagger_auto_schema(tags=["[Groups] Groups"], operation_description="설명입니다")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[Groups] Groups"], operation_description="설명입니다")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[Groups] Groups"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[Groups] Groups"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[Groups] Groups"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[Groups] Groups"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
