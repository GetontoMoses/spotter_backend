"""Views for the accounts app."""

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trip, LocationUpdate, DailyLog
from .serializers import TripSerializer, LocationUpdateSerializer, DailyLogSerializer
import requests
from rest_framework import status
import datetime
from config.settings.utils import get_env_variable

ORS_API_KEY = get_env_variable("ORS_API_KEY")

class TripListCreateView(ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        trip = serializer.save()
        try:
            route_data = self.get_route(trip.pickup_location, trip.dropoff_location)

            trip.total_distance = (
                route_data.get("features")[0]["properties"]["summary"]["distance"]
                / 1609.34
            )
            trip.estimated_hours = (
                route_data.get("features")[0]["properties"]["summary"]["duration"]
                / 3600
            )
            trip.save()

        except Exception as e:
            print(f"Error fetching route: {e}")

    def get_route(self, start, end):
        start_coords = self.geocode(start)
        end_coords = self.geocode(end)

        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {"Authorization": ORS_API_KEY}
        params = {
            "start": f"{start_coords[0]},{start_coords[1]}",
            "end": f"{end_coords[0]},{end_coords[1]}",
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def geocode(self, location_name):
        url = "https://api.openrouteservice.org/geocode/search"
        params = {"api_key": ORS_API_KEY, "text": location_name}
        response = requests.get(url, params=params).json()
        coords = response["features"][0]["geometry"]["coordinates"]
        return coords  # [longitude, latitude]


class LocationUpdateListCreateView(ListCreateAPIView):
    queryset = LocationUpdate.objects.all()
    serializer_class = LocationUpdateSerializer


class DailyLogListView(ListCreateAPIView):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer


class TripLogsByTripView(APIView):
    def get(self, request, trip_id):
        updates = LocationUpdate.objects.filter(trip_id=trip_id).order_by("timestamp")
        serializer = LocationUpdateSerializer(updates, many=True)
        return Response(serializer.data)
