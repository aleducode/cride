"""Circles View"""
# Django Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Permissions
from cride.permissions.circles import IsCircleAdmin
# Serializer
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership


class CirclesViewset(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Circle view set"""

    serializer_class = CircleModelSerializer

    def get_queryset(self):
        """Restrict list to public-only"""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        """Assign circle admin"""
        circle = serializer.save()
        user = self.request.user
        Membership.objects.create(
            user=user,
            circle=circle,
            is_admin=True,
            remaining_invitations=10,
        )

    def get_permissions(self):
        """Assign permissions for each action"""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permision() for permision in permissions]

