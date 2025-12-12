import os
from uuid import uuid4
from geopy.geocoders import GoogleV3
import asyncio

import logging

from agent_traveler.libs.places import PlacesService


def get_places(data: dict[str, any]):
    places = []
    for f in data["flights"]:
        departure = f.get("departure_airport")
        if departure:
            f["departure_loc_ref"] = str(uuid4())
            places.append(
                {
                    "name": departure,
                    "type": "airport",
                    "address": "",
                    "reference": [f["departure_loc_ref"]],
                }
            )
        else:
            logging.warning(f"Missing departude airport [{f["flight_number"]}]")
        arrival = f.get("arrival_airport")
        if arrival:
            f["arrival_loc_ref"] = str(uuid4())
            places.append(
                {
                    "name": arrival,
                    "type": "airport",
                    "address": "",
                    "reference": [f["arrival_loc_ref"]],
                }
            )
        else:
            logging.warning(f"Missing arrival airport [{f["flight_number"]}]")

    for h in data["hotels"]:
        h["loc_ref"] = str(uuid4())
        places.append(
            {
                "name": h["name"],
                "type": "hotel",
                "address": h["address"],
                "reference": [h["loc_ref"]],
            }
        )

    for c in data["car_rents"]:
        c["pickup_loc_ref"] = str(uuid4())
        places.append(
            {
                "name": c["name"],
                "type": "car_rental",
                "address": c["pickup_address"],
                "reference": [c["pickup_loc_ref"]],
            }
        )
        c["dropoff_loc_ref"] = str(uuid4())
        places.append(
            {
                "name": c["name"],
                "type": "car_rental",
                "address": c["dropoff_address"],
                "reference": [c["dropoff_loc_ref"]],
            }
        )

    return places


def get_place_info(p, place_search):
    fields = ["formattedAddress", "id", "photos", "location", "types"]
    try:
        info = place_search.find_place_from_text(
            ", ".join([p["type"], p["name"], p["address"]]), fields=fields
        )

        p["address"] = info["address"]
        p["place_id"] = info["place_id"]
        p["photos"] = info["photos"]
        p["latitude"] = info["latitude"]
        p["longitude"] = info["longitude"]
        p["types"] = info["types"]
        p["map_url"] = info["map_url"]
    except Exception as e:
        p["place_id"] = ""
        p["photos"] = []
        p["latitude"] = ""
        p["longitude"] = ""
        p["types"] = []
        p["map_url"] = []
        logging.error(f"Error find_place_from_text [{e}]")
        logging.debug(p)


async def get_places_info(places):
    place_search = PlacesService()
    tasks = [asyncio.to_thread(get_place_info, p, place_search) for p in places]

    await asyncio.gather(*tasks)

    return places


def remove_duplicates(places):
    place_list = dict()
    for p in places:
        if not p["place_id"]:
            continue
        if not p["place_id"] in place_list:
            place_list[p["place_id"]] = p
            continue

        p_in = place_list[p["place_id"]]
        p_in["reference"].extend(p["reference"])

    return list(place_list.values())


def get_place_timezone_info(place, geolocator):
    try:
        if not place["latitude"] or not place["longitude"]:
            logging.warning(f"Missing latitude/longitude [{place['name']}]")
            logging.debug(place)
            return
        timezone = geolocator.reverse_timezone((place["latitude"], place["longitude"]))
        place["timezone"] = timezone.pytz_timezone.zone
    except Exception as e:
        place["timezone"] = ""
        logging.error(f"Error getting timezone [{e}]")
        logging.debug(place)


async def get_places_timezone_info(places):
    geolocator = GoogleV3(api_key=os.getenv("GOOGLE_PLACES_API_KEY"))
    tasks = [asyncio.to_thread(get_place_timezone_info, p, geolocator) for p in places]

    await asyncio.gather(*tasks)

    return places


def get_place_by_reference(reference, places):
    for p in places:
        if reference in p["reference"]:
            return p

    logging.warning(f"Place reference not found [{reference}]")
    return None


def update_extracted_data(data, places):
    for f in data["flights"]:
        departure_place = get_place_by_reference(f["departure_loc_ref"], places)
        f["departure_timezone"] = (
            departure_place["timezone"]
            if departure_place and departure_place["timezone"]
            else ""
        )
        arrival_place = get_place_by_reference(f["arrival_loc_ref"], places)
        f["arrival_timezone"] = (
            arrival_place["timezone"]
            if arrival_place and arrival_place["timezone"]
            else ""
        )

    for h in data["hotels"]:
        hotel_place = get_place_by_reference(h["loc_ref"], places)
        h["timezone"] = (
            hotel_place["timezone"] if hotel_place and hotel_place["timezone"] else ""
        )

    for c in data["car_rents"]:
        pickup_place = get_place_by_reference(c["pickup_loc_ref"], places)
        c["pickup_timezone"] = (
            pickup_place["timezone"]
            if pickup_place and pickup_place["timezone"]
            else ""
        )
        dropoff_place = get_place_by_reference(c["dropoff_loc_ref"], places)
        c["dropoff_timezone"] = (
            dropoff_place["timezone"]
            if dropoff_place and dropoff_place["timezone"]
            else ""
        )

    return data


async def improve_extracted_data(data):
    places = get_places(data)
    places = await get_places_info(places)
    places = remove_duplicates(places)
    places = await get_places_timezone_info(places)
    data = update_extracted_data(data, places)

    return data, places


def place_tool(
    place,
    search_query: str,
    fields: list[str] = ["formattedAddress", "id", "photos", "location", "types"],
):
    try:
        places_service = PlacesService()
        result = places_service.find_place_from_text(search_query, fields)
        for k, v in result.items():
            place[k] = v
    except Exception as e:
        logging.error(f"Place tool error [{e}]")
        logging.debug(place)

    return place


def update_highlight(h, dest):
    new_place = {
        "name": h,
        "address": ", ".join([dest["name"], dest["country"]]),
        "type": "highlights",
        "place_id": "",
        "map_url": "",
        "latitude": "",
        "longitude": "",
        "reference": dest["reference"],
    }
    return place_tool(new_place, ", ".join([h, new_place["address"]]))


def update_destination(dest):
    new_dest = {
        "name": dest["name"],
        "address": ", ".join([dest["name"], dest["country"]]),
        "type": "city",
        "place_id": "",
        "map_url": "",
        "latitude": "",
        "longitude": "",
        "reference": dest["reference"],
    }
    return place_tool(new_dest, new_dest["address"])


async def extract_places_destination(destinations):
    places = []

    for dest in destinations:
        try:
            highlights = dest.get("highlights", [])
            dest["reference"] = str(uuid4())
            tasks = [asyncio.to_thread(update_destination, dest)] + [
                asyncio.to_thread(update_highlight, h, dest) for h in highlights
            ]
            new_places = await asyncio.gather(*tasks)
            places.extend(new_places)
        except Exception as e:
            logging.error(f"Destination error [{dest["name"]}]")
            logging.debug(dest)

    return places
