"""Circles urls."""

from django.urls import path

from cride.circles.views import list_circles

urlpatterns=[
    path('circles/',list_circles)

]