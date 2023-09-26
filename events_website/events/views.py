from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from events.models import Event
from events.serializers import EventSerializer, EventCreateSerializer
from events.swagger_decription import response_schema_event, result_patch_del


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'post', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return EventCreateSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(
        responses={201: response_schema_event},
    )
    def create(self, request,  *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event: Event = serializer.save(author=request.user)
        return Response(EventSerializer(event).data)

    @swagger_auto_schema(
        request_body=EventCreateSerializer(),
        responses={200: response_schema_event},
    )
    def partial_update(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        if request.user == event.author:
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied(
                detail="You are not the author of the event",
            )

    @swagger_auto_schema(
        request_body=no_body,
        responses={200: result_patch_del('You have joined the event')},
    )
    @action(detail=True, methods=['patch'])
    def join(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        event.participants.add(request.user)
        return Response(data="You have joined the event")

    @swagger_auto_schema(
        request_body=no_body,
        responses={200: result_patch_del('You have left the event')},
    )
    @action(detail=True, methods=['delete'])
    def leave(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        event.participants.remove(request.user)
        return Response(data="You have left the event")

    @swagger_auto_schema(
        request_body=no_body,
        responses={200: result_patch_del('Event deleted')},
    )
    def destroy(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        if request.user == event.author:
            event.delete()
            return Response(data="Event deleted")
        else:
            raise PermissionDenied(
                detail="You are not the author of the event",
            )
