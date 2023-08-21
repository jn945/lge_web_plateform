from django.urls import include, path, register_converter
from rest_framework import routers

from .views import VirtualAnalysisRequestViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(
    "virtual-analysis-request",
    VirtualAnalysisRequestViewSet,
    basename="VirtualAnalysisRequestViewSet",
)


urlpatterns = [
    path("api/v1/", include(router.urls)),
]
