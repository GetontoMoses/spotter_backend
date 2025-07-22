"""URL Configuration for the trips app."""

from django.urls import path
from .views import TripPlannerView


urlpatterns = [path("create/", TripPlannerView.as_view(), name="new_trip")]
