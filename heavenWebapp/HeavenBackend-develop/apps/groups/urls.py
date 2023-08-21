from django.urls import include, path
from rest_framework import routers

from .views import GroupViewSet

router = routers.DefaultRouter()
router.register(r"groups", GroupViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
