"""
Tool research about places to get its latitude, longitude (and more) using
the Google Places (new) API
"""

import os
from typing import Dict, List, Any
from google.adk.tools import ToolContext
from .artifact import save_kml_tool

import simplekml
import requests


defaultFields = ["formattedAddress", "id", "photos", "location"]


class PlacesService:
    """Wrapper to Places API."""

    def __init__(self, api_key: str = ""):
        self.places_api_key = api_key if api_key else os.getenv("GOOGLE_PLACES_API_KEY")
        if not self.places_api_key:
            raise RuntimeError("Missing API Key")

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
                    out["id"] = place_details["id"]
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


# Google Places API
places_service = PlacesService()


def place_tool(place, search_query: str, fields: list[str] = defaultFields):
    try:
        result = places_service.find_place_from_text(search_query, fields)
        for k, v in result.items():
            place[k] = v
    except Exception as e:
        print(e)

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

        return {
            "status": "success",
            "places": places,
            "message": "Place information was updated correctly",
        }
    except Exception as e:
        print(f"Error calling map_tool {e}")
        return {"status": "error", "message": f"Exception called! {e}"}


def update_places_with_destinations(tool_context: ToolContext):
    destinations = tool_context.state.get("destination_data", dict()).get(
        "destination_data"
    )
    if not destinations:
        return []

    places = tool_context.state["extracted_data"].get("places", [])
    for dest in destinations:
        highlights = dest.get("highlights", [])
        for h in highlights:
            new_place = {
                "name": h,
                "address": ", ".join([dest["name"], dest["country"]]),
                "type": "highlights",
                "place_id": "",
                "map_url": "",
                "lat": "",
                "long": "",
            }
            places.append(new_place)
            place_tool(new_place, ", ".join([h, new_place["address"]]))

    return places


def create_kml(places_list):
    kml = simplekml.Kml()

    for place in places_list:
        pnt = kml.newpoint(
            name=place.get("name"),
            coords=[(place.get("long"), place.get("lat"))],
        )

        pnt.description = f"Place ID: {place.get('place_id')}"
        pnt.extendeddata.newdata(name="place_id", value=place.get("place_id"))

    return kml.kml()


async def create_map_points(tool_context: ToolContext):
    """
    Create a file of type KML with the places, to be imported to Google My Maps.
    The output will be saved at a persistent storage.

    Args:
        tool_context: The ADK tool context.

    Returns:
        The status of the operation, with data
    """
    out = map_tool(tool_context)
    if out["status"] == "error":
        return out

    places = out["places"]

    places_hightlights = update_places_with_destinations(tool_context)
    places.extend(places_hightlights)

    places = [
        p for p in places if "lat" in p and "long" in p and p["lat"] and p["long"]
    ]
    if len(places) > 0:
        output = create_kml(places)
        await save_kml_tool(output, tool_context)
        return {"status": "success", "message": "create KML file", "kml": output}

    return {"status": "error", "message": "No data to create map place"}
