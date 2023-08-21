from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from modules.common.viewset import CustomViewset
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


# 회원가입
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(tags=["[User] User"], operation_description="설명입니다")
    def createuser(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserViewset(CustomViewset):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(tags=["[User] User"], operation_description="설명입니다")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[User] User"], operation_description="설명입니다")
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors)

        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[User] User"], operation_description="설명입니다")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[User] User"], operation_description="설명입니다")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[User] User"], operation_description="설명입니다")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["[User] User"], operation_description="설명입니다")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
