"""Circles Views"""
#django
from django.http import JsonResponse
#RestFramework
from rest_framework.decorators import api_view
from rest_framework.response import Response
#models
from cride.circles.models import Circle
#serializers
from cride.circles.serializers import CircleSerializer

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
    name=request.data['name']
    slug_name=request.data['slug_name']
    #no required field
    about=request.data.get('about','')
    circle=Circle.objects.create(name=name,slug_name=slug_name,about=about)
    data={
            'name':circle.name,
            'slug_name':circle.slug_name,
            'about':circle.about,
            'rides_taken':circle.rides_taken,
            'rides_offered':circle.rides_offered,
            'members_limit':circle.members_limit,
         
        }
    return Response(data)
