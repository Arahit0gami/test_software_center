from rest_framework.routers import SimpleRouter

from events.views import EventViewSet

events_router = SimpleRouter()

events_router.register(
    'event',
    EventViewSet,
    basename='event'
)
