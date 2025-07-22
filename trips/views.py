"""Views for the accounts app."""

from rest_framework import generics
from .serializers import TripSerializer
from .models import Trip


class TripPlannerView(generics.ListCreateAPIView):
    """view for creating a new trip"""
    
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
