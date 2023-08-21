"""heaven URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

schema_view = get_schema_view(
    openapi.Info(
        title="LG TV",
        default_version="0.1.0",
        # description="해당 문서 설명(예: humanscape-project API 문서)",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="이메일"), # 부가정보
        # license=openapi.License(name="mit"),     # 부가정보
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.document.urls")),
    path("", include("apps.CommonCode.urls")),
    path("", include("apps.HWSpec.urls")),
    path("", include("apps.accounts.urls")),
    path("", include("apps.groups.urls")),
    path("", include("apps.prm.urls")),
    path("", include("apps.measurement.urls")),
    path("", include("apps.virtualanalysis.urls")),
    path("", include("apps.HWCheck.urls")),
    path("", include("apps.webapp.urls")),
    path("swagger", csrf_exempt(schema_view.with_ui("swagger", cache_timeout=0))),
    path("redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", include("apps.testapp.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
