"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import SimpleRouter

from server.apps.comment.views import CommentViewSet
from server.apps.group.views import GroupViewSet
from server.apps.topic.views import TopicViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
]

# Auth URLs

urlpatterns += [
    path("api/auth/", include("server.apps.user.urls")),
]

# DRF Router for ViewSets

router = SimpleRouter()

router.register(r"groups", GroupViewSet)
router.register(r"topics", TopicViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns += [
    path("api/", include(router.urls)),
]

# DRF YASG (Yet Another Swagger Generator)

schema_view = get_schema_view(
    openapi.Info(
        title="E-Campus API",
        default_version="v1",
        description="API for e-campus project",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    permission_classes=[],
    public=True,
)

urlpatterns += [
    path(
        "api/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger",
    ),
]

# Media and Static files

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
