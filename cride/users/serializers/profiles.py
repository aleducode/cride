"""Profiles Serializers."""

# Django Rest Framework
from rest_framework import serializers

# Model
from cride.users.models import User, Profile

# Utilities
from datetime import timedelta
import jwt


class ProfileModelSerializer(serializers.ModelSerializer):
    """profile model serializer"""

    class Meta:
        model = Profile
        fields = (
            'picture',
            'biography',
            'rides_taken',
            'rides_offered',
            'reputation',
        )
        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'reputation',
        )

