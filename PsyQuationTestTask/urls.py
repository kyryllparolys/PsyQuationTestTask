from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


class CategorizedAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys):
        if len(operation_keys) >= 1:
            operation_keys = operation_keys[1:]
        return super().get_tags(operation_keys)


schema_view = get_schema_view(
    openapi.Info(
      title="PsyQuation Test Task",
      default_version='v1.0.0',
    ),
    permission_classes=(AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs', schema_view.with_ui(), name='docs'),
    path('api/', include('transactions.urls')),
    path('api/', include('accounts.urls'))
]
