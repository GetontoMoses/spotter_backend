from geopy.geocoders import Nominatim
import requests
from django.conf import settings


def geocode_location(location):
    """
    Converts a human-readable location string (e.g. "Chicago") into GPS coordinates (lon, lat).
    Uses Nominatim from the OpenStreetMap project.
    """
    geolocator = Nominatim(user_agent="eld_trip_app") 
    location_data = geolocator.geocode(location)

    # Return [lon, lat] — the order required by ORS
    return [location_data.longitude, location_data.latitude]


def get_route_info(start, waypoint, end):
    """
    Uses the OpenRouteService (ORS) API to calculate:
    - Total distance
    - Duration
    - Route polyline coordinates
    """

    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": settings.ORS_API_KEY}

    coords = [
        geocode_location(start),
        geocode_location(waypoint),
        geocode_location(end),
    ]

    data = {"coordinates": coords, "format": "geojson"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        route = response.json()
        segment = route["features"][0]["properties"]["segments"][0]
        distance_km = segment["distance"] / 1000
        duration_hr = segment["duration"] / 3600
        geometry = route["features"][0]["geometry"]["coordinates"]

        return {
            "distance_km": round(distance_km, 2),
            "duration_hr": round(duration_hr, 2),
            "geometry": geometry,
        }

    return None


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
