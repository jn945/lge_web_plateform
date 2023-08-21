# Create your views here.
import os

import modules.common.file_transfer as file_transfer
from apps.accounts.models import User
from django.http import FileResponse
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


class FileUploadFsView(views.APIView):
    parser_classes = (MultiPartParser,)
    queryset = User.objects.all()

    @swagger_auto_schema(
        operation_description="uploaded_file_to_fs",
        tags=["[TEST]"],
        manual_parameters=[
            openapi.Parameter(
                name="file_data",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="The file to be uploaded.",
            ),
        ],
    )
    @action(detail=False, methods=["post"])
    def post(self, request, *args, **kwargs):
        file_transfer.uploaded_file_to_fs(request, "./data")
        return Response("File processed successfully.")


class FileUploadBytesView(views.APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description="uploaded_file_to_bytes",
        tags=["[TEST]"],
        manual_parameters=[
            openapi.Parameter(
                name="file_data",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="The file to be uploaded.",
            ),
        ],
    )
    @action(detail=False, methods=["post"])
    def post(self, request, *args, **kwargs):
        return Response(bytes.hex(file_transfer.uploaded_file_to_bytes(request)))


class FileDownLoadBytesView(views.APIView):
    @swagger_auto_schema(
        operation_description="download_bytes",
        tags=["[TEST]"],
    )
    @action(detail=False, methods=["get"])
    def get(self, request, *args, **kwargs):
        data = b"test data"
        return file_transfer.download_bytes(data, "test.txt")


class FileDownLoadCsvView(views.APIView):
    @swagger_auto_schema(
        operation_description="downlod_csv",
        tags=["[TEST]"],
    )
    @action(detail=False, methods=["get"])
    def get(self, request, *args, **kwargs):
        data = [
            ["Name", "Age", "City"],
            ["John", "30", "New York"],
            ["Jane", "25", "Los Angeles"],
            ["Mike", "35", "Chicago"],
        ]
        return file_transfer.downlod_csv(data, "test.csv")


class FileDownLoadFileView(views.APIView):
    @swagger_auto_schema(
        operation_description="download_file",
        tags=["[TEST]"],
        manual_parameters=[
            openapi.Parameter(
                name="path",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="path",
            ),
        ],
    )
    @action(detail=False, methods=["get"])
    def get(self, request, *args, **kwargs):
        path = request.query_params.get("path")
        file_path = os.path.join(".","data", path)
        print(file_path)
        if file_path and os.path.exists(file_path):
            file = open(file_path, "rb")
            response = FileResponse(file)
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
