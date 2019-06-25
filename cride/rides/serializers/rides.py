"""Ride Serializers."""

# Django Rest Framework
from rest_framework import serializers

# Models
from cride.rides.models import Ride

# Utilities
from datetime import timedelta
from django.utils import timezone


class CreateRideSerializer(serializers.ModelSerializer):
    """Create Ride Serializer."""
    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        """Meta class"""

        model = Ride
        exclude = ('offered_in', 'passengers', 'rating', 'is_active')

    def validate_departure_date(self, data):
        """Validate date is not in the pass"""
        min_date = timezone.now() + timedelta(minutes=10)
        if data < min_date:
            raise serializers.ValidationError(
                'Departure time must be at least pass in the next 20 minutes window.'
            )
        return data

