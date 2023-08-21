from django.urls import include, path, register_converter
from rest_framework import routers

from .views import (
    CommonCodeViewSet,
    FileDownLoadBytesView,
    FileDownLoadCsvView,
    FileDownLoadFileView,
    FileUploadBytesView,
    FileUploadFsView,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register("common-code", CommonCodeViewSet, basename="Common_code")


urlpatterns = [
    path("api/v1/upload-fs", FileUploadFsView.as_view()),
    path("api/v1/upload-bytes", FileUploadBytesView.as_view()),
    path("api/v1/download-bytes", FileDownLoadBytesView.as_view()),
    path("api/v1/download-csv", FileDownLoadCsvView.as_view()),
    path("api/v1/download-file", FileDownLoadFileView.as_view()),
    path("api/v1/", include(router.urls)),
]
