from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Medium API",
        default_version='v1',
        description="Test description",
    ),
    public=False,
    permission_classes=(IsAuthenticated, )
)
