from django.urls import include, path

from .views import (
    FileDownLoadBytesView,
    FileDownLoadCsvView,
    FileDownLoadFileView,
    FileUploadBytesView,
    FileUploadFsView,
)

urlpatterns = [
    path("api/v1/test/uploadfs", FileUploadFsView.as_view()),
    path("api/v1/test/uploadbytes", FileUploadBytesView.as_view()),
    path("api/v1/test/downloadbytes", FileDownLoadBytesView.as_view()),
    path("api/v1/test/downloadcsv", FileDownLoadCsvView.as_view()),
    path("api/v1/test/downloadfile", FileDownLoadFileView.as_view()),
]
