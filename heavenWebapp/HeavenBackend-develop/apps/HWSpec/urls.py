from django.urls import include, path, register_converter
from rest_framework import routers

from .views import (  # PowerInfoViewSet,; PowerViewSet,
    SocCompareViewSet,
    SocInfoViewSet,
    SocSearchViewSet,
    SocViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register("hw-spec/info", SocInfoViewSet, basename="hw-spec-info")
router.register("hw-spec", SocViewSet, basename="hw-spec")
# router.register('hw-check/power',PowerViewSet)
# router.register('hw-check/power-info',PowerInfoViewSet)


urlpatterns = [
    # compare
    path(
        "api/v1/hw-spec/comparison/<int:pk>",
        SocCompareViewSet.as_view({"delete": "delete_compare"}),
    ),
    path(
        "api/v1/hw-spec/comparison",
        SocCompareViewSet.as_view({"get": "get_compare", "put": "put_compare"}),
    ),
    path(
        "api/v1/hw-spec/comparison_id_list",
        SocCompareViewSet.as_view({"get": "get_compare_id_list"}),
    ),
    # search
    path(
        "api/v1/hw-spec/search",
        SocSearchViewSet.as_view({"get": "get_search", "put": "put_search"}),
    ),
    # search_id_list
    path(
        "api/v1/hw-spec/search_id_list",
        SocSearchViewSet.as_view({"get": "get_search_id_list"}),
    ),
    # router
    path("api/v1/", include(router.urls)),
]
