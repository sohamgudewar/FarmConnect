import googlemaps
import os
from typing import List, Optional, Tuple
from backend.schemas.location import NearbyPlace

class MapsService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if self.api_key:
            self.gmaps = googlemaps.Client(key=self.api_key)
        else:
            self.gmaps = None

    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Converts an address string into (latitude, longitude)."""
        if not self.gmaps:
            return None
        
        try:
            geocode_result = self.gmaps.geocode(address)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return location['lat'], location['lng']
        except Exception as e:
            print(f"Geocoding error: {e}")
        return None

    def get_nearby_places(self, lat: float, lng: float, query: str = "APMC", radius: int = 50000) -> List[NearbyPlace]:
        """Finds nearby places based on a query (e.g., 'APMC' or 'Tractor repair')."""
        if not self.gmaps:
            return []

        try:
            places_result = self.gmaps.places(query=query, location=(lat, lng), radius=radius)
            places = []
            for result in places_result.get('results', []):
                places.append(NearbyPlace(
                    name=result['name'],
                    address=result.get('formatted_address', ''),
                    latitude=result['geometry']['location']['lat'],
                    longitude=result['geometry']['location']['lng'],
                    place_id=result['place_id']
                ))
            return places
        except Exception as e:
            print(f"Places search error: {e}")
        return []

    def calculate_distance(self, origin: Tuple[float, float], destination: Tuple[float, float]) -> Optional[float]:
        """Calculates the distance in kilometers between two points."""
        if not self.gmaps:
            return None

        try:
            matrix = self.gmaps.distance_matrix(origin, destination, mode="driving")
            if matrix['status'] == 'OK':
                element = matrix['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    # distance is in meters, convert to km
                    return element['distance']['value'] / 1000.0
        except Exception as e:
            print(f"Distance matrix error: {e}")
        return None

maps_service = MapsService()
