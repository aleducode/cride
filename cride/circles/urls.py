"""Circles urls."""

# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from circles.views import circles as circle_views
router = DefaultRouter()
router.register(r'circles', circle_views.CirclesViewset, base_name='circle')

urlpatterns = [
    path('', include(router.urls)),
]
