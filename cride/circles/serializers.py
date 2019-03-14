"""Circle Serializers """

#Rest Framework
from rest_framework import serializers

class CircleSerializer(serializers.Serializer):
    """Circle serializer"""
    
    name=serializers.CharField()
    slug_name=serializers.SlugField()
    rides_taken=serializers.IntegerField()
    rides_offered=serializers.IntegerField()
    members_limit=serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
    """Create Circle"""
    name=serializers.CharField(max_lenght=140)
    slug_name=serializers.SlugField(max_lenght=140)
    about=serializers.CharField(
        max_lenght=255,
        required=False)