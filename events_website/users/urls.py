from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, UserRegisterView, UserLoginView, \
    UserLogoutView, UserBaseView

users_router = SimpleRouter()

users_router.register(
    'user',
    UserViewSet,
    basename='user'
)

url_templates = [
    path('', UserBaseView.as_view(), name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

]