"""Circles urls."""

from django.urls import path

from cride.circles.views import list_circles,create_circle,import_csv


urlpatterns=[
    path('circles/',list_circles),
    path('prueba/',import_csv),
    path('circles/create',create_circle),


]