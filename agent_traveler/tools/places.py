import os
from typing import Dict, List, Any
from google.adk.tools import ToolContext

import requests


class PlacesService:
    """Wrapper to Placees API."""

    def _check_key(self):
        if (
            not hasattr(self, "places_api_key") or not self.places_api_key
        ):  # Either it doesn't exist or is None.
            # https://developers.google.com/maps/documentation/places/web-service/get-api-key
            self.places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    def find_place_from_text(self, query: str) -> Dict[str, str]:
        """Fetches place details using a text query."""
        self._check_key()
        places_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": query,
            "inputtype": "textquery",
            "fields": "place_id,formatted_address,name,photos,geometry",
            "key": self.places_api_key,
        }

        try:
            response = requests.get(places_url, params=params)
            response.raise_for_status()
            place_data = response.json()

            if not place_data.get("candidates"):
                return {"error": "No places found."}

            # Extract data for the first candidate
            place_details = place_data["candidates"][0]
            place_id = place_details["place_id"]
            place_name = place_details["name"]
            place_address = place_details["formatted_address"]
            photos = self.get_photo_urls(place_details.get("photos", []), maxwidth=400)
            map_url = self.get_map_url(place_id)
            location = place_details["geometry"]["location"]
            lat = str(location["lat"])
            lng = str(location["lng"])

            return {
                "place_id": place_id,
                "place_name": place_name,
                "place_address": place_address,
                "photos": photos,
                "map_url": map_url,
                "lat": lat,
                "lng": lng,
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Error fetching place data: {e}"}

    def get_photo_urls(
        self, photos: List[Dict[str, Any]], maxwidth: int = 400
    ) -> List[str]:
        """Extracts photo URLs from the 'photos' list."""
        photo_urls = []
        for photo in photos:
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={maxwidth}&photoreference={photo['photo_reference']}&key={self.places_api_key}"
            photo_urls.append(photo_url)
        return photo_urls

    def get_map_url(self, place_id: str) -> str:
        """Generates the Google Maps URL for a given place ID."""
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"


# Google Places API
places_service = PlacesService()


def place_tool(place, search_query: str):
    result = places_service.find_place_from_text(search_query)
    # Fill the place holders with verified information.
    place["place_id"] = result["place_id"] if "place_id" in result else None
    place["map_url"] = result["map_url"] if "map_url" in result else None
    if "lat" in result and "lng" in result:
        place["lat"] = result["lat"]
        place["long"] = result["lng"]

    return place


def map_tool(tool_context: ToolContext):
    """
    This is going to inspect all the places at the state variable and try to update its information.
    One by one it will retrieve the accurate Lat/Lon from the Map API, if the Map API is available for use.

    Args:
        tool_context: The ADK tool context.

    Returns:
        The updated state with the full JSON object.
    """
    try:
        places = tool_context.state.get("extracted_data", dict()).get("places", [])
        for place in places:
            place_tool(
                place, ", ".join([place["type"], place["name"], place["address"]])
            )
        tool_context.state["extracted_data"]["places"] = places

        # destinations = tool_context.state.get("destination_data", [])
        # for dest in destinations:
        #     plcs = dest.get("places", [])
        #     for p in plcs:
        #         place_tool(p, ", ".join(p["name"], p["country"]))
        #     dest["places"] = plcs
        # tool_context.state["destination_data"] = destinations

        # return places, destinations
        return places
    except Exception as e:
        print(f"Error calling map_tool {e}")
        return {"status": "error", "message": f"Exception called! {e}"}
