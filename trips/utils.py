from geopy.geocoders import Nominatim
import requests
from django.conf import settings
from config.settings.utils import get_env_variable
from .models import DailyLog 

def geocode_location(location):
    """
    Converts a human-readable location string (e.g. "Chicago") into GPS coordinates (lon, lat).
    Uses Nominatim from the OpenStreetMap project.
    """
    geolocator = Nominatim(user_agent="eld_trip_app") 
    location_data = geolocator.geocode(location)

    # Return [lon, lat] — the order required by ORS
    return [location_data.longitude, location_data.latitude]


def get_route_info(start_coords, pickup_coords, dropoff_coords):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    coordinates = [start_coords, pickup_coords, dropoff_coords]

    headers = {
        "Authorization": get_env_variable("ORS_API_KEY"),
        "Content-Type": "application/json",
    }

    response = requests.post(url, json={"coordinates": coordinates}, headers=headers)

    try:
        route = response.json()
    except ValueError:
        raise ValueError("Invalid JSON response from ORS")

    # 🔍 Print the full response for debugging
    print("ORS Response:", route)

    if response.status_code != 200:
        raise ValueError(f"ORS API error: {route}")

    if "features" not in route:
        raise ValueError(f"Expected 'features' key not found. Response: {route}")

    segment = route["features"][0]["properties"]["segments"][0]
    distance = segment["distance"]  # in meters
    duration = segment["duration"]  # in seconds

    return {
        "distance_km": round(distance / 1000, 2),
        "duration_hours": round(duration / 3600, 2),
        "geometry": route["features"][0]["geometry"],
    }


def plan_fuel_stops(distance_km):
    """
    Calculates fuel stops assuming 1 stop every 1000 miles.
    """
    return int(distance_km // 1609) + 1


def generate_eld_logs(total_drive_hours, cycle_hours_used):
    """
    Generates daily logs based on 70 hr/8-day cycle and 11-hr max driving/day.
    Returns a list of dicts with driving, on-duty, off-duty hours per day.
    """
    logs = []
    remaining_cycle = 70 - cycle_hours_used
    day = 1

    while total_drive_hours > 0 and remaining_cycle > 0:
        drive_today = min(11, total_drive_hours, remaining_cycle)
        on_duty = drive_today + 1  # Includes 1hr at pickup/dropoff
        off_duty = 24 - on_duty
        
        # Simulating 24-hour status log
        for hour in range(24):
            if hour < drive_today:
                status = 'driving'
            elif hour < on_duty:
                status = 'on_duty'
            else:
                status = 'off_duty'
            DailyLog.objects.create(trip=trip, day=day, hour=hour, status=status)

        logs.append(
            {
                "day": day,
                "driving": round(drive_today, 2),
                "on_duty": round(on_duty, 2),
                "off_duty": round(off_duty, 2),
            }
        )

        total_drive_hours -= drive_today
        remaining_cycle -= drive_today
        day += 1

    return logs
