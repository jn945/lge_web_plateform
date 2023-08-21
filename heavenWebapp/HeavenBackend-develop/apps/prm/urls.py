from django.urls import include, path
from rest_framework import routers

from .views import (
    PlanGroupInfoViewSet,
    PlanGroupViewSet,
    PlanInfoViewSet,
    PlanSeriesViewSet,
    PlanViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register(
    r"plan/(?P<plan_id>\d+)/plan-group", PlanGroupViewSet, basename="plan-group"
)
router.register(
    r"plan-group-info",
    PlanGroupInfoViewSet,
    basename="plan-group-info",
)
router.register(r"plan/(?P<plan_id>\d+)/series", PlanSeriesViewSet)
router.register("plan/info", PlanInfoViewSet)
router.register("plan", PlanViewSet)

urlpatterns = [
    path(
        "api/v1/plan/group-name-duplication",
        PlanGroupViewSet.as_view({"get": "duplication"}),
        name="duplication",
    ),
    path("api/v1/", include(router.urls)),
]
