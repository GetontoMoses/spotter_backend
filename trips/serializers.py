"""Serializers for the trips app."""

from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
