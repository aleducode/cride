"""Circles Views"""
#django
from django.http import JsonResponse
#RestFramework
from rest_framework.decorators import api_view
from rest_framework.response import Response
#models
from cride.circles.models import Circle
#serializers
from cride.circles.serializers import (
    CircleSerializer,
    CreateCircleSerializer)

import csv

def import_csv(request):
    with open('circles.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            circle = Circle(**row)
            circle.save()
            print(circle.name)



@api_view(['GET'])
def list_circles(request):
    """list manual api example"""
    circles=Circle.objects.filter(is_public=True)
    serializers=CircleSerializer(circles,many=True)
    return Response(serializers.data)

@api_view(['POST'])
def create_circle(request):
    """Create circle"""
    serializer=CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle=serializer.save()
    return Response(CircleSerializer(circle).data)
