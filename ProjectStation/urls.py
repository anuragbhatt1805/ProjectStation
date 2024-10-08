"""
URL configuration for ProjectStation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from core.views import ChangePassword


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='api-schema'),
         name='redoc'),
    path('api/v2/ping/', lambda request: JsonResponse({'connection': True})),
    path('api/v2/change-password/', ChangePassword.as_view(), name='change_password'),
    path('api/v2/user/', include('core.urls')),
    path('api/v2/fabricator/', include('fabricator.urls')),
    path('api/v2/department/', include('department.urls')),
    path('api/v2/vendor/', include('vendor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )