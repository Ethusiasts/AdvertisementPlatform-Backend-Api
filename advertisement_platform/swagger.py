from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Advertisement Platform Api",
        default_version='v1',
        description="Advertisement Platform Api Documentation",
    ),
    public=True,
)
