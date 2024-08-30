from rest_framework.routers import DefaultRouter
from django.urls import include, path
from core.views import (
    UserLoginApiView
)

router = DefaultRouter()


urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('', include(router.urls))
]