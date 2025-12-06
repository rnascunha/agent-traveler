from typing import Dict, List, Any
import requests
import os

defaultFields = ["formattedAddress", "id", "photos", "location", "types"]


class PlacesService:
    """Wrapper to Places API."""

    def __init__(self, api_key: str = ""):
        self.places_api_key = api_key if api_key else os.getenv("GOOGLE_PLACES_API_KEY")
        if not self.places_api_key:
            raise RuntimeError("Missing GOOGLE_PLACES_API_KEY key")

    def find_place_from_text(
        self, query: str, fields: list[str] = defaultFields
    ) -> Dict[str, str]:
        """Fetches place details using a text query."""

        if len(fields) == 0:
            raise Exception("No fields selected")

        url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.places_api_key,
            "X-Goog-FieldMask": "places." + ",places.".join(fields),
        }
        data = {"textQuery": query}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        place_data = response.json()

        if len(place_data["places"]) == 0:
            raise Exception("No places found")

        out = dict()
        place_details = place_data["places"][0]

        for f in fields:
            match f:
                case "displayName":
                    out[f] = place_details["displayName"]["text"]
                case "photos":
                    out[f] = self.get_photo_urls(
                        place_details.get("photos", []), maxwidth=400
                    )
                case "location":
                    location = place_details["location"]
                    out["lat"] = str(location["latitude"])
                    out["long"] = str(location["longitude"])
                case "formattedAddress":
                    out["address"] = place_details["formattedAddress"]
                case "id":
                    out["place_id"] = place_details["id"]
                    out["map_url"] = self.get_map_url(place_details["id"])
                case _:
                    out[f] = place_details[f]

        return out

    def get_photo_urls(
        self, photos: List[Dict[str, Any]], maxwidth: int = 400
    ) -> List[str]:
        """Extracts photo URLs from the 'photos' list."""
        photo_urls = []
        for photo in photos:
            photo_url = f"https://places.googleapis.com/v1/{photo["name"]}/media?maxWidthPx={maxwidth}&key={self.places_api_key}"
            photo_urls.append(photo_url)
        return photo_urls

    def get_map_url(self, place_id: str) -> str:
        """Generates the Google Maps URL for a given place ID."""
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
