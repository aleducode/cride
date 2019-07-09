"""Ride Serializers."""

# Django Rest Framework
from rest_framework import serializers

# Models
from cride.circles.models import Membership
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

    def validate(self, data):
        """General validation."""
        if self.context['request'].user != data['offered_by']:
            raise serializers.ValidationError('Rides offered in behalf of others are not allowed.')
        user = data['offered_by']
        circle = self.context['circle']
        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
                )
            self.context['membership'] = membership
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')
        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('Departure date must happend after arrival date.')
        return data

    def create(self, data):
        """Upgrade ride and stats"""
        circle = self.context['circle']
        ride = Ride.objects.create(**data, offered_in=circle)

        # Circle
        circle.rides_offered += 1
        circle.save()

        # Membership
        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()

        # Profile
        profile = data['offered_by'].profile
        profile.rides_offered += 1
        profile.save()

        return ride

