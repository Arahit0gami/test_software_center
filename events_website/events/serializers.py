from django.contrib.auth import get_user_model
from rest_framework import serializers

from events.models import Event
from users.models import User

User: User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class EventSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)
    participants = UserSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['author', 'participants', 'date_create']


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title', 'text', 'date_event',)

    def create(self, validated_data):
        event = Event.objects.create(
            **validated_data
        )
        event.save()

        return event
