from django.urls import include, path
from rest_framework import routers, urls

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewset)
urlpatterns =[
    path('',include(router.urls)),
    #path('users/signup/', views.UserCreate.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]