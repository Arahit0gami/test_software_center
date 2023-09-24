from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import RegisterSerializer, UserLoginSerializer
from .swagger_description import response_schema


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    authentication_classes = []
    permission_classes = []
    serializer_classes = {
        'login': UserLoginSerializer,
        'register': RegisterSerializer,
    }

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]

    @swagger_auto_schema(
        request_body=no_body,
        deprecated=True,
        responses={405: "Method Not Allowed"}
    )
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('post')

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: response_schema},
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer: RegisterSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: CustomUser = serializer.save()
        return Response(
            data=self.result_with_token(user),
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: response_schema},
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer: UserLoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["login"],
            password=serializer.validated_data["password"]
        )
        if isinstance(user, CustomUser):
            return Response(data=self.result_with_token(user))
        else:
            raise ValidationError("Invalid login or password")

    @staticmethod
    def result_with_token(user: CustomUser) -> dict:
        token, created = Token.objects.get_or_create(user=user)
        result = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_of_birth": user.date_of_birth,
            "date_joined": user.date_joined,
            "token": token.key,
        }
        return result
