"""Circle Membership Views"""

# Django Rest Framework
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

# Model
from cride.circles.models import Circle, Membership, Invitation

# Serializer
from cride.circles.serializers import MembershipModelSerializer, AddMemberSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember, IsSelfMember


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
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
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActiveCircleMember)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
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

    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):
        """Retrieve a member's inivitations

        Will return a list containing all the memebers that
        have used its invitations and another list containing
        the invitations that haven't used yet"""
        member = self.get_object()
        invited_members = Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True
        )
        unused_invitations = Invitation.objects.filter(
            circle=self.circle,
            issued_by=request.user,
            used=False
        ).values_list('code')
        #  number of invitations available to create
        diff = member.remaining_invitations - len(unused_invitations)
        invitations = [x[0] for x in unused_invitations]
        for i in range(0, diff):
            invitations.append(
            Invitation.objects.create(
                issued_by=request.user,
                circle=self.circle
            ).code
            )

        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': invitations
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = AddMemberSerializer(
            data=request.data,
            context={'circle': self.circle, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)


