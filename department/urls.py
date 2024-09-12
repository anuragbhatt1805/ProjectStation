from rest_framework.routers import DefaultRouter
from django.urls import include, path
from department.views import DepartmentViewSet

router = DefaultRouter()
router.register('', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls))
]