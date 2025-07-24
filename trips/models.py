"""Models for the trips app."""

from django.db import models


class Trip(models.Model):
    current_location = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    cycle_hours_used = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    dvir_number = models.CharField(max_length=100, blank=True)
    manifest_number = models.CharField(max_length=100, blank=True)
    shipper = models.CharField(max_length=100, blank=True)
    commodity = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.current_location} → {self.dropoff_location}"


class DailyLog(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="daily_logs")
    day = models.IntegerField()  # Day index of the trip
    hour = models.IntegerField()  # Hour of the day (0–23)

    status = models.CharField(
        max_length=20,
        choices=[
            ("off_duty", "Off Duty"),
            ("sleeper", "Sleeper Berth"),
            ("driving", "Driving"),
            ("on_duty", "On Duty (Not Driving)"),
        ],
    )

    def __str__(self):
        return f"Trip {self.trip.id} - Day {self.day} Hour {self.hour} → {self.status}"
