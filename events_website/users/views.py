from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from events.models import Event
from events.serializers import EventSerializer
from .forms import UserRegisterForm, UserLoginForm
from .models import User
from .serializers import RegisterSerializer, UserLoginSerializer, \
    UserBaseSerializer
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
        security=[],
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer: RegisterSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        return Response(
            data=self.result_with_token(user),
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: response_schema},
        security=[],
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer: UserLoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["login"],
            password=serializer.validated_data["password"]
        )
        if isinstance(user, User):
            return Response(data=self.result_with_token(user))
        else:
            raise ValidationError("Invalid login or password")

    @staticmethod
    def result_with_token(user: User) -> dict:
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



# --------------------------------------------------------------------------
"""
Код ниже идет, для задания в части визуальных страниц с использование форм и js
"""


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """

    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'registration/registration.html'
    next_page = 'home'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.next_page)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """

    form_class = UserLoginForm
    template_name = 'registration/login.html'
    next_page = 'home'
    success_message = 'Добро пожаловать на сайт!'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """

    next_page = 'home'


class UserBaseView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    login_url = 'login'
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
            except Exception:
                return JsonResponse(data={}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse(
                UserBaseSerializer(user).data, safe=False
            )
        context = self.get_context_data(**kwargs)
        context['title'] = 'Информация о событиях'
        context['user'] = request.user
        return self.render_to_response(context)


class EventsBaseView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        all_events = EventSerializer(Event.objects.all(), many=True).data
        return JsonResponse(all_events, safe=False)

    def put(self, request):
        event_id = request.GET.get('id')
        event = get_object_or_404(Event, pk=event_id)
        event.participants.add(request.user)
        return JsonResponse(data={"result": True})

    def delete(self, request):
        event_id = request.GET.get('id')
        event = get_object_or_404(Event, pk=event_id)
        event.participants.remove(request.user)
        return JsonResponse(data={"result": True})
