"""Users views."""

# Django Rest Framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializaer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    ProfileModelSerializer)

# Models
from cride.users.models import User
from cride.circles.models import Circle

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from cride.users.permissions import IsAccountOwner


# TODO: documentate @actionr replace to old methods
class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.

    Handle login, signup and account validation.
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializaer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permission based on action"""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action == ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializaer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User signup"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializaer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification"""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {'message': 'Congratulations, now go share some rides!'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Account verification"""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializaer(user).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True,
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response
