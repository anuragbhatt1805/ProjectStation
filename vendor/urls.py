from rest_framework.routers import DefaultRouter
from django.urls import include, path
from vendor.views import VendorModelViewSet

router = DefaultRouter()
router.register('', VendorModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]