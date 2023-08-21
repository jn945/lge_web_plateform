from django.urls import include, path, register_converter
from rest_framework import routers

from .views import (
    DocumentHistoryApiview,
    DocumentHistoryApiviewList,
    DocumentPrevicousHistoryViewSet,
    DocumentViewSet,
    HWCheckInfoViewSet,
    HWCheckRowViewSet,
    HWCheckViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register("hw-check/info", HWCheckInfoViewSet, basename="hw-check")

router.register(
    r"hw-check/(?P<hw_check_id>\d+)/row/(?P<hw_check_row_id>\d+)/document",
    DocumentViewSet,
    basename="document",
)
router.register(
    r"hw-check/(?P<hw_check_id>\d+)/row", HWCheckRowViewSet, basename="hw-check-row"
)

router.register("hw-check", HWCheckViewSet, basename="hw-check")


urlpatterns = [
    path(
        "api/v1/hw-check/<int:hw_check_id>/row/<int:hw_check_row_id>/document/<int:document_id>/previous-history/<int:document_history_id>",
        DocumentPrevicousHistoryViewSet.as_view(),
    ),
    path(
        "api/v1/hw-check/<int:hw_check_id>/row/<int:hw_check_row_id>/document/<int:document_id>/history/<int:document_history_id>",
        DocumentHistoryApiview.as_view(),
        name="document-history-retrieve",
    ),
    path(
        "api/v1/hw-check/<int:hw_check_id>/row/<int:hw_check_row_id>/document/<int:document_id>/history",
        DocumentHistoryApiviewList.as_view(),
        name="document-history",
    ),
    path(
        "api/v1/hw-check/<int:hw_check_id>/row/<int:hw_check_row_id>/document",
        DocumentViewSet.as_view(
            {"delete": "delete_id_list", "get": "list", "post": "create"}
        ),
        name="delete-id-list",
    ),
    path("api/v1/", include(router.urls)),
]
