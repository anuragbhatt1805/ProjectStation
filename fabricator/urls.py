from rest_framework.routers import DefaultRouter
from django.urls import include, path
from fabricator.views import FabricatorModelViewSet

router = DefaultRouter()
router.register('', FabricatorModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]