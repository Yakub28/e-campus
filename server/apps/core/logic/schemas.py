from drf_yasg import openapi

BAD_REQUEST = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "field_name": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING),
        ),
    },
)

UNAUTHORIZED = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "detail": openapi.Schema(type=openapi.TYPE_STRING),
    },
)
