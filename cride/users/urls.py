"""Urls urls."""

# Django
from django.urls import path

# Views
from cride.users.views import UserLoginAPIView


urlpatterns = [
    path('login', UserLoginAPIView.as_view(), name='login'),
]
