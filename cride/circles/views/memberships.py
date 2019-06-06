"""Circle Membership Views"""

# Django Rest Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Model
from cride.circles.models import Circle
from cride.circles.models import Membership

# Serializer
from cride.circles.serializers import MembershipModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Circle membership view set"""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exist"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Asign permissions for each action"""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        return [p() for p in permissions]

    def get_queryset(self):
        """Return membership"""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )

    def get_object(self):
        """Return the circle member by using the username"""
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            circle=self.circle,
            is_active=True
        )

    def perform_destroy(self, instance):
        """Deactivate membership"""
        instance.is_active = False
        instance.save()
