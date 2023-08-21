from django.urls import include, path, register_converter
from rest_framework import routers

from .views import ProductSpecificationViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(
    "document/product-specification", ProductSpecificationViewSet, basename="hw-check"
)


urlpatterns = [
    path(
        "pdf",
        ProductSpecificationViewSet.as_view({"get": "return_pdf"}),
        name="product-specification-pdf",
    ),
    path("api/v1/", include(router.urls)),
]
