"""Users views."""

# Django Rest Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializaer,
    UserSignUpSerializer
)


class UserLoginAPIView(APIView):
    """Users login API view"""

    def post(self, request, *args, **kwargs):
        """Handle HTTP Post Request"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializaer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserSignUpAPIView(APIView):
    """Users login API view"""

    def post(self, request, *args, **kwargs):
        """Handle HTTP Post Request"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializaer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
