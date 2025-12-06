import json
from pprint import pprint
import sys
import os
from uuid import uuid4
from geopy.geocoders import GoogleV3
from dotenv import load_dotenv
import asyncio

sys.path.insert(1, os.path.realpath(os.path.curdir))

from agent_traveler.tools.places import PlacesService

load_dotenv()


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
        print(p["name"])
        p["address"] = info["address"]
        p["place_id"] = info["place_id"]
        p["photos"] = info["photos"]
        p["lat"] = info["lat"]
        p["long"] = info["long"]
        p["types"] = info["types"]
        p["map_url"] = info["map_url"]
    except Exception as e:
        p["place_id"] = ""
        p["photos"] = []
        p["lat"] = ""
        p["long"] = ""
        p["types"] = []
        p["map_url"] = []
        print(f"Error places: {p}")
        print(e)


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
        if not place["lat"] or not place["long"]:
            return
        timezone = geolocator.reverse_timezone((place["lat"], place["long"]))
        place["timezone"] = timezone.pytz_timezone.zone
    except Exception as e:
        place["timezone"] = ""

    print(f"{place["name"]}: {place["timezone"]}")


async def get_places_timezone_info(places):
    geolocator = GoogleV3(api_key=os.getenv("GOOGLE_PLACES_API_KEY"))
    tasks = [asyncio.to_thread(get_place_timezone_info, p, geolocator) for p in places]

    await asyncio.gather(*tasks)

    return places


def get_place_by_reference(reference, places):
    for p in places:
        if reference in p["reference"]:
            return p

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
    data = update_extracted_data(extract_data, places)

    return data, places


if __name__ == "__main__":

    data_extracted_path = "./data/output/state_extracted.json"
    data_extracted_updated_path = "./data/output/state_extracted_updated.json"

    with open(data_extracted_path, "r") as file:
        data = file.read()

    extract_data = json.loads(data)["extracted_data"]

    extract_data, places = asyncio.run(improve_extracted_data(extract_data))

    pprint(extract_data)

    with open(data_extracted_updated_path, "w") as wfile:
        extract_data_json = json.dumps(extract_data)
        wfile.write(extract_data_json)
