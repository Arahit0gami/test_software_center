from drf_yasg import openapi

error_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
    }
)

user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name of the user'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the user'),
    }
)

event_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Event ID'),
        'author': user_schema,
        'participants': openapi.Schema(type=openapi.TYPE_ARRAY, items=user_schema, description='Participants of the event'),
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title name of the event'),
        'text': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the event'),
        'date_event': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Date when the event'),
        'date_create': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Date when the event create'),
    }
)

response_schema_event = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': error_schema,
        'result': event_schema,
    }
)


def result_patch_del(text: str):
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': error_schema,
            'result': openapi.Schema(
                type=openapi.TYPE_STRING,
                description=text
            ),
        }
    )
