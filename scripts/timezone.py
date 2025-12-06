import sys
import os

sys.path.insert(1, os.path.realpath(os.path.curdir))

import json
from geopy.geocoders import GeoNames, Nominatim, GoogleV3
from pprint import pprint

data_path = "./data/output/state.json"

# geolocator = GeoNames(username="rnascunha")
# geolocator = Nominatim(user_agent="my_app")
geolocator = GoogleV3(api_key="AIzaSyAzc5KxfL49CEcjUu1U3BAdiZADWsFTUQo")

address = "London, UK"
address = "Paris, FR"
# address = "Lake Annecy"
address = "Eurico Salles (VIX)"
# address = "175 5th Avenue"
# address = "Palace of the Dukes of Burgundy, Dijon, France"
# address = "1 Rue Rameau, 21000 Dijon, France"
# address = "Maison de la Magie"
# address = "Esc. Denis Papin, 41000 Blois, France"
# components={"city": "Paris", "country": "FR"}
# address="Amasebailu, Karnataka, India"
try:
    # location = geolocator.geocode(address)

    # print("Full structured output (raw dictionary):")
    # pprint(location.raw)

    # Access common attributes directly
    # print("\nAccessing common attributes:")
    # print(f"Address: {location.address}")
    # print(f"Latitude: {location.latitude}")
    # print(f"Longitude: {location.longitude}")

    # # Access specific structured components from the raw dictionary
    # print("\nAccessing specific components from the raw dictionary:")
    # address_components = location.raw.get("address", {})
    # print(f"City: {address_components.get('city')}")
    # print(f"Postcode: {address_components.get('postcode')}")
    # print(f"State: {address_components.get('state')}")

    print("\nTimezone:")
    timezone = geolocator.reverse_timezone((45.058049399999994, 7.6361104))
    # timezone = geolocator.reverse_timezone(address)
    pprint(timezone.pytz_timezone.zone)
    print("--------------")
    pprint(timezone.raw)
except Exception as e:
    print(f"Error: {e}")

# def get_time_data():
#     with open(data_path, "r") as file:
#         data = file.read()

#     data_json = json.loads(data)
#     extracted_data = data_json["extracted_data"]

#     for f in extracted_data["flights"]:
#         dict
#         print(f)


# get_time_data()
