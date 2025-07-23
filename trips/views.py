"""Views for the accounts app."""

from rest_framework import generics,status
from rest_framework.response import response
from .serializers import TripSerializer
from .models import Trip
from .utils import get_route_info, plan_fuel_stops, generate_eld_logs


class TripPlannerView(generics.ListCreateAPIView):
    """
    Handles POST requests to plan a trip and return route info and ELD logs.
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def create(self, request, *args, **kwargs):
        # Serialize and validate the input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()

        # Get routing data from utils.py
        route_data = get_route_info(
            trip.current_location,
            trip.pickup_location,
            trip.dropoff_location
        )

        if not route_data:
            return Response({"error": "Failed to get route. Please check locations."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Generate fuel stops and logs
        fuel_stops = plan_fuel_stops(route_data["distance_km"])
        eld_logs = generate_eld_logs(
            total_drive_hours=route_data["duration_hr"],
            cycle_hours_used=trip.cycle_hours_used
        )

        # Create combined response
        return Response({
            "trip": serializer.data,
            "route": {
                "distance_km": route_data["distance_km"],
                "duration_hr": route_data["duration_hr"],
                "coordinates": route_data["geometry"],
                "estimated_fuel_stops": fuel_stops
            },
            "eld_logs": eld_logs
        }, status=status.HTTP_201_CREATED)
