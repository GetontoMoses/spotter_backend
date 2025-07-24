"""Models for the trips app."""

from django.db import models


class Trip(models.Model):
    driver_name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.driver_name}'s Trip from {self.start_location} to {self.destination}"


class LogEntry(models.Model):
    STATUS_CHOICES = [
        ("driving", "Driving"),
        ("on_duty", "On Duty"),
        ("off_duty", "Off Duty"),
        ("sleeper birth", "sleeper birth"),
     
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="logs")
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.trip.driver_name}: {self.status} from {self.start_time} to {self.end_time}"
