from rest_framework.routers import DefaultRouter
from django.urls import include, path
from core.views import (
    UserLoginApiView,
    ClientModelViewSet,
    StaffModelViewSet,
    VendorUserModelViewSet,
    UserModelViewSet
)

router = DefaultRouter()
router.register('client', ClientModelViewSet)
router.register('staff', StaffModelViewSet)
router.register('vendor', VendorUserModelViewSet)
router.register('', UserModelViewSet)


urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('', include(router.urls))
]