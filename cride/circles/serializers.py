"""Circle Serializers """

# Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# models
from cride.circles.models import Circle


class CircleSerializer(serializers.Serializer):
    """Circle serializer"""

    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
    """Create Circle"""
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=140,
        # unique field respect circles objecs
        validators=[
            UniqueValidator(queryset=Circle.objects.all())
        ])
    about = serializers.CharField(
        max_length=255,
        required=False)

    def create(self, data):
        """Create and save circle"""
        return Circle.objects.create(**data)
