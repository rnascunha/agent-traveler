from fastkml import kml
from fastkml.styles import Style, IconStyle
from fastkml.data import SimpleData, ExtendedData
from pygeoif.geometry import Point
import zipfile

# https://developers.google.com/maps/documentation/places/web-service/icons#places-api-new
iconList = [
    {
        "value": ["airport", "international_airport"],
        "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/airport_pinlet.svg",
        "icon_png": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/airport_pinlet.png",
        "color": "FF00FF00",
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
        "color": "ffff0000",
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
    elif type in iconMap:
        return iconMap[type]
    return generic_icon


def create_style_id(place):
    return "#" + place["place_id"]


def create_style(place):
    iconDef = get_icon_color(place)
    style = Style(
        styles=[
            IconStyle(icon_href=iconDef["icon_png"], color=iconDef["color"]),
        ],
    )

    return style


def create_point(place):
    images_html = "".join([f'<img src="{url}">' for url in place["photos"]])
    extendeddata = ExtendedData(
        elements=[SimpleData(name="place_id", value=place["place_id"])]
    )

    style = create_style(place)

    placemarks = kml.Placemark(
        id=place["place_id"],
        name=place["name"],
        description=f"<div>{images_html}</div>",
        geometry=Point(float(place["longitude"]), float(place["latitude"]), 0.0),
        extended_data=extendeddata,
        styles=[style],
    )
    return placemarks


def create_cities_layers(places_list, doc):
    cities = {p["reference"]: p for p in places_list if p["type"] == "city"}
    highlights = {p["reference"]: [] for p in places_list if p["type"] == "highlights"}
    for k in highlights.keys():
        highlights[k] = [
            p for p in places_list if p["type"] == "highlights" and p["reference"] == k
        ]

    for k, place in cities.items():
        folder = kml.Folder(name=place["name"])
        doc.append(folder)

        pnt = create_point(place)
        folder.append(pnt)
        for hplace in highlights.get(k, []):
            pnt2 = create_point(hplace)
            folder.append(pnt2)


def create_kml(places_list):
    k = kml.KML()

    d = kml.Document(
        id="docid",
        name="My trip",
        description="This awesome trip",
    )
    k.append(d)

    f = kml.Folder(
        name="Trip information", description="Information of airports, hotels..."
    )
    d.append(f)

    for place in filter(lambda x: x["type"] not in ["city", "highlights"], places_list):
        f.append(create_point(place))
    create_cities_layers(places_list, d)

    return k.to_string(prettyprint=True)


def create_kmz_file(kml_file: str, filename: str):
    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(kml_file, arcname=kml_file)
