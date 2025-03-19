"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import TodoAPIView

schema_view = get_schema_view(
   openapi.Info(
      title="Todos API",
      default_version='v1',
      description="Create todo for your daily tasks",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="musah.sesitech@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
   authentication_classes = [],
)

urlpatterns = [
    ### admin site
    path('admin/', admin.site.urls),

    ### Default API view
    path('', TodoAPIView.as_view(), name='TodoAPI'),
    #### Auth Views
    path('api/auth/', include('authentication.urls')),
    ### Todos Views
    path('api/todo/', include('todo.urls')),

    ### Swagger UI (DOCUMENTATION)re_
    re_path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
