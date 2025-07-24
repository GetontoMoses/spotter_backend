"""Serializers for the trips app."""

from rest_framework import serializers
from .models import Trip, DailyLog


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class DailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLog
        fields = ["trip", "day", "hour", "status"]
