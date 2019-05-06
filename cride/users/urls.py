"""Urls urls."""

# Django
from django.urls import path

# Views
from cride.users.views import UserLoginAPIView, UserSignUpAPIView


urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('signup/', UserSignUpAPIView.as_view(), name='signup'),
]
