from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from authrest import urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve
from DynamicForms import urls as url1
from backend_Rest import settings

schema_view = get_schema_view(
    openapi.Info(
        title="DynamicForms",
        default_version='v1',
        description="Test description",
        terms_of_service="policies",
        contact=openapi.Contact(email="contact@example.local"),
        license=openapi.License(name="development Env"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("authentication/", include(urls)),
                  path("dynamicforms/", include(url1)),
                  url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
              ] + [
                  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

              ]
