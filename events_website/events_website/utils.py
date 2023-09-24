from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            'error': response.data,
            'result': None
        }
    return response


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'error' not in data and 'result' not in data:
            data = {'error': None, 'result': data}
        return super().render(data, accepted_media_type, renderer_context)
