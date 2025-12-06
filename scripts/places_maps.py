import sys
import os

sys.path.insert(1, os.path.realpath(os.path.curdir))

from agent_traveler.tools.places import PlacesService
import json
import simplekml
from dotenv import load_dotenv
import math

load_dotenv()

data_path = "./data/output/state.json"
data_places_path = "./data/output/places_updated.json"
data_kml_path = "./data/output/maps_updated.kml"
data_kmz_path = "./data/output/maps_updated.kmz"


def update_places():
    fields = ["id", "types", "addressComponents"]

    with open(data_path, "r") as file:
        raw = file.read()
        data = json.loads(raw)
        places = data["extracted_data"]["places"]

    service = PlacesService()
    for place in places:
        try:
            print(place["name"])
            p = service.find_place_from_text(
                ", ".join([place["name"], place["address"]]), fields=fields
            )
            place["place_id"] = p["place_id"]
            place["types"] = p["types"]
            place["addressComponents"] = p["addressComponents"]
        except Exception as e:
            print(e)

    data_json = json.dumps(places)
    with open(data_places_path, "w") as wfile:
        wfile.write(data_json)


# https://developers.google.com/maps/documentation/places/web-service/icons#places-api-new
iconList = [
    {
        "value": ["airport", "international_airport"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/airport_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/airport_pinlet.png",
        # "icon_png": "https://storage.googleapis.com/agent-traveler/airport_icon_circle.png",
        "color": "ff00ffaa",
    },
    {
        "value": ["car_rental"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/bus_share_taxi_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/bus_share_taxi_pinlet.png",
        "color": "ff0000ff",
    },
    {
        "value": ["hotel", "lodging", "extended_stay_hotel", "resort_hotel"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet.png",
        "color": "ffffaaaa",
    },
    {
        "value": ["park", "garden", "hiking_area", "sports_activity_location"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/tree_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/tree_pinlet.png",
        "color": "ff00ff00",
    },
    {
        "value": ["zoo"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/paw_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/paw_pinlet.png",
        "color": "ff00ff00",
    },
    {
        "value": ["museum"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/museum_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/museum_pinlet.png",
        "color": "ff2244aa",
    },
    {
        "value": ["historical_landmark", "historical_place"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/historic_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/historic_pinlet.png",
        "color": "ff00bb00",
    },
    {
        "value": ["restaurant", "food"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/restaurant_pinlet.png",
        "color": "ffbbaa00",
    },
    {
        "value": ["church", "place_of_worship"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/worship_christian_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/worship_christian_pinlet.png",
        "color": "ff666666",
    },
    {
        "value": ["performing_arts_theater", "event_venue"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/theater_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/theater_pinlet.png",
        "color": "ffff0000",
    },
    {
        "value": ["point_of_interest", "tourist_attraction"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/monument_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/monument_pinlet.png",
        "color": "ffff0000",
    },
]

generic_icon = {
    "value": ["generic"],
    "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet.svg",
    "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet.png",
    "color": "ffff0000",
}


def create_icon_map():
    map = dict()
    for i in iconList:
        for v in i["value"]:
            map[v] = i
    return map


iconMap = create_icon_map()


def get_icon_color(place):
    type = place["type"].lower().replace(" ", "_")
    if type == "highlights":
        for t in place["types"]:
            if t in iconMap:
                return iconMap[t]
    else:
        return iconMap[type]
    return generic_icon


def generate_circle_coords(lat, lon, radius_meters, num_points=64):
    """
    Generates a list of coordinates forming a circle around a center point.

    Args:
        lat, lon: Center coordinates (degrees).
        radius_meters: Radius of the circle in meters.
        num_points: How many sides the polygon has (more = smoother).

    Returns:
        List of tuples [(lon, lat), (lon, lat), ...]
    """
    coords = []
    earth_radius = 6378137.0  # Earth's radius in meters (WGS84)

    # Convert center to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    # Loop through degrees (0 to 360) to create points
    for i in range(num_points + 1):  # +1 to close the loop
        # Current angle in radians
        angle = math.pi * 2 * i / num_points

        # Calculate offset in radians
        d_lat = (radius_meters / earth_radius) * math.cos(angle)
        d_lon = (radius_meters / earth_radius) * math.sin(angle) / math.cos(lat_rad)

        # New coordinates in degrees
        new_lat = lat + math.degrees(d_lat)
        new_lon = lon + math.degrees(d_lon)

        coords.append((new_lon, new_lat))

    return coords


def create_kml(places_list):
    kml = simplekml.Kml()

    for place in places_list:
        pnt = kml.newpoint(
            name=place.get("name"),
            coords=[(place.get("long"), place.get("lat"))],
        )

        # pnt.style.iconstyle.scale = 1.2
        iconDef = get_icon_color(place)
        pnt.style.iconstyle.icon.href = iconDef["icon_png"]
        pnt.style.iconstyle.color = iconDef["color"]
        # pnt.style.balloonstyle.text = "Test ballon"
        # pnt.style.balloonstyle.bgcolor = simplekml.Color.lightgreen
        # pnt.style.balloonstyle.textcolor = simplekml.Color.aqua

        images_html = ""
        for url in place["photos"]:
            images_html += f'<img src="{url}" width="300" style="margin-bottom:10px; border-radius:5px;"><br>'

        # pnt.description = f"Place ID: {place.get('place_id')}"
        pnt.description = f"<div>{images_html}</div>"
        pnt.extendeddata.newdata(name="place_id", value=place.get("place_id"))

        # circle_coords = generate_circle_coords(
        #     float(place.get("lat")), float(place.get("long")), 500
        # )
        # pol = kml.newpolygon(name=f"500m Radius")
        # pol.outerboundaryis = circle_coords

        # # 3. Style the Circle (Semi-transparent Fill)
        # # Color format: AABBGGRR (7f = ~50% transparency)
        # pol.style.polystyle.color = "7f0000ff"  # Semi-transparent Red
        # pol.style.linestyle.color = "ff0000ff"  # Solid Red Outline
        # pol.style.linestyle.width = 2

    kml.savekmz(data_kmz_path)
    return kml.kml()


def remove_duplicates(places):
    places_dict = dict()
    for p in places:
        places_dict[p["place_id"]] = p
    return list(places_dict.values())


def create_kml_map():
    with open(data_places_path, "r") as file:
        data = file.read()

    places = remove_duplicates(json.loads(data))
    kml_data = create_kml(places)

    # with open(data_kml_path, "w") as wfile:
    #     wfile.write(kml_data)


# print("Updating...")
# update_places()
print("Creating maps...")
create_kml_map()
