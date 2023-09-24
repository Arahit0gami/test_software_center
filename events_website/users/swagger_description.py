from drf_yasg import openapi

error_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
    }
)

result_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name of the user'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the user'),
        'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Date of birth of the user'),
        'date_joined': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Date when the user joined'),
        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication token for the user'),
    }
)

response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': error_schema,
        'result': result_schema,
    }
)