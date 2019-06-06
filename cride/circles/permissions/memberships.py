"""Mermbership permissions classes"""

# Django Rest Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """Allow access only to circle members."""

    def has_permission(self, request, view):
        """Verify user is an active member of the circle"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True,
            )
        except Membership.DoesNotExist:
            return False
        return True
