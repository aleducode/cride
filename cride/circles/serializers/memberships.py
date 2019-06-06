"""Membership serializer"""

# Django Rest Framework
from rest_framework import serializers

# Model
from cride.circles.models import Membership

# Serializer
from cride.users.serializers import UserModelSerializaer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model Serializer"""

    joined_at = serializers.DateTimeField(source='created', read_only=True)
    user = UserModelSerializaer(read_only=True)
    invited_by = serializers.StringRelatedField()

    class Meta:
        model = Membership
        fields = (
            'user',
            'is_admin', 'is_active',
            'used_invitations', 'remaining_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
            'joined_at'
        )
        read_only = (
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
        )

