from django.urls import include, path
from rest_framework import routers

from .views import (
    MeasurementRequestViewSet,
    ResultHistoryApiview,
    ResultHistoryApiviewList,
    ResultViewset,
    TestItemInfoViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register("testitem-info", TestItemInfoViewSet)
router.register("measurement-request", MeasurementRequestViewSet)
router.register("measurement-result", ResultViewset)

urlpatterns = [
    path(
        "api/v1/measurement-result/<int:result_id>/history/<int:id>",
        ResultHistoryApiview.as_view(),
        name="document-history-retrieve",
    ),
    path(
        "api/v1/measurement-result/<int:result_id>/history",
        ResultHistoryApiviewList.as_view(),
        name="result-history",
    ),
    path("api/v1/", include(router.urls)),
]
