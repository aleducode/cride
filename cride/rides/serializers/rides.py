"""Ride Serializers."""

# Django Rest Framework
from rest_framework import serializers

# Models
from cride.circles.models import Membership
from cride.rides.models import Ride
from cride.users.models import User

# Serializer
from cride.users.serializers import UserModelSerializer

# Utilities
from datetime import timedelta
from django.utils import timezone


class RideModelSerializer(serializers.ModelSerializer):
    """Ride model serializer"""
    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField()
    passengers = UserModelSerializer(read_only=True, many=True)

    class Meta:
        """Meta class"""
        model = Ride
        fields = '__all__'
        read_only_fields = (
            'offered_in',
            'offered_by',
            'rating',
        )

    def update(self, instance, data):
        """Allow update only before departure date."""
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializer.ValidationError('Ongoing rides cannot be modified.')
        return super(RideModelSerializer, self).update(instance, data)


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


class JoinRideSerializer(serializers.ModelSerializer):
    """Join ride serializer"""

    passenger = serializers.IntegerField()

    class Meta:
        """Meta class."""
        model = Ride
        fields = ('passenger',)

    def validate_passenger(self, data):
        """Verify passenger exist and it is circle member"""
        try:
            user = User.objects.get(pk=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Passenger')

        circle = self.context['circle']
        try:
            member = Membership.objects.get(user=user, circle=circle, is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        self.context['user'] = user
        self.context['member'] = member
        return data

    def validate(self, data):
        """Verify ride allow new passengers."""
        ride = self.context['ride']
        if self.context['ride'].departure_date <= timezone.now():
            raise serializers.ValidationError('You cannot join this ride right now.')

        if ride.available_seats == 0:
            raise serializers.ValidationError('Ride is already full!')

        if Ride.objects.filter(passengers__pk=data['passenger']) == 0:
            raise serializers.ValidationError('Passenger is already in this trip.')

        return data

    def update(self, instance, data):
        """Add passenger to ride and update stats."""
        ride = self.context['ride']
        user = self.context['user']
        circle = self.context['circle']
        member = self.context['member']

        # many to many relationship
        ride.passengers.add(user)

        # Profile
        profile = user.profile
        profile.rides_taken += 1
        profile.save()

        # Membership
        member.rides_taken += 1
        member.save()

        # Cirlce
        circle.rides_taken += 1
        circle.save()

        return ride


class EndRideSerializer(serializers.ModelSerializer):
    """End ride serializer."""
    current_time = serializers.DateTimeField()

    class Meta:
        model = Ride
        fields = ('is_active', 'current_time')

    def validate_current_time(self, data):
        """Verify ride have indeed started."""
        ride = self.context['view'].get_object()
        if data <= ride.departure_date:
            raise serializers.ValidationError("Ride has not started yet.")
        return data
