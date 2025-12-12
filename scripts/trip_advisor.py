import requests
import os
from typing import Literal, Tuple
from dotenv import load_dotenv

load_dotenv()


class TripAdvisorAPI:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key if api_key else os.getenv("TRIP_ADVISOR_API_KEY")
        if not self.api_key:
            raise Exception("Api key 'TRIP_ADVISOR_API_KEY' not set")

    def search_nearby(self, latitude: float, longitude: float):
        url = "https://api.content.tripadvisor.com/api/v1/location/nearby_search?latLong={latitude},{longitude}&language=en&key={self.api_key}"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        return response

    def search(
        self,
        address: str,
        *,
        category: Literal["hotels", "attractions", "restaurants", "geos"] = "",
        latLong: Tuple[float, float] = None,
    ):
        url = f"https://api.content.tripadvisor.com/api/v1/location/search?searchQuery={address}&language=en&key={self.api_key}"

        if category:
            url += f"&category={category}"

        if latLong:
            url += f"&latLong={latLong[0]},{latLong[1]}"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        return response


if __name__ == "__main__":
    latitude = -20.261641700000002
    longitude = -40.2833237
    search = TripAdvisorAPI()
    response = search.search_nearby(latitude, longitude)
    print(response.text)

    response = search.search(
        "vitoria,brasil", category="attractions", latLong=(latitude, longitude)
    )
    print(response.text)
