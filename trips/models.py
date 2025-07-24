"""Models for the trips app."""

from django.db import models


class Trip(models.Model):
    current_location = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    cycle_hours_used = models.FloatField()
    total_distance = models.FloatField(null=True, blank=True)
    estimated_hours = models.FloatField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Trip from {self.pickup_location} to {self.dropoff_location}"


class LocationUpdate(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="location_updates"
    )
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Off Duty", "Off Duty"),
            ("Sleeper Birth", "Sleeper Birth"),
            ("Driving", "Driving"),
            ("On Duty", "On Duty"),
        ],
    )

    def __str__(self):
        return f"{self.status} at {self.location} ({self.timestamp})"


class DailyLog(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="daily_logs")
    date = models.DateField()
    log_image_url = models.URLField(
        blank=True, null=True
    )  