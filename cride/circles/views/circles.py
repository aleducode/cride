"""Circles View"""
# Django Rest Framework
from rest_framework import viewsets

# Serializer
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle


class CirclesViewset(viewsets.ModelViewSet):
    """Circle view set"""

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
