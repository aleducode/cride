"""Rides Url"""

# Django
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import rides as rides_view

router = DefaultRouter()
router.register(
    r'circles/(?<slug_name>[-a-zA-Z0-0_]+)/rides',
    rides_view.RidesViewSet,
    basename='ride'
)
urlpatterns = [
    path('', include(router.urls)),
]

