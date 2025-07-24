"""URL Configuration for the trips app."""

from django.urls import path
from .views import (
    TripListCreateView,
    LocationUpdateListCreateView,
    TripLogsByTripView,
    DailyLogListView,
)

urlpatterns = [
    path("create/", TripListCreateView.as_view(), name="trip-list-create"),
    path(
        "locations/",
        LocationUpdateListCreateView.as_view(),
        name="location-update-list-create",
    ),
    path("logs/<int:trip_id>/", TripLogsByTripView.as_view(), name="trip-logs"),
    path("dailylogs/", DailyLogListView.as_view(), name="daily-logs"),
]
