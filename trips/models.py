"""Models for the trips app."""

from django.db import models

class Trip(models.Model):
    current_location = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    cycle_hours_used = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.current_location} → {self.dropoff_location}"
