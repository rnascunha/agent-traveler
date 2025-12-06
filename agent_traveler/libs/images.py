import os
import requests


class UnsplashImage:
    """
    Wrapper of Unsplash API

    documentation: https://unsplash.com/documentation
    """

    def __init__(self, *, app_id: str = "", access_key: str = "", secret_key: str = ""):
        self.app_id = app_id if app_id else os.getenv("UNSPLASH_APP_ID")
        self.access_key = access_key if access_key else os.getenv("UNSPLASH_ACCESS_KEY")
        self.secret_key = secret_key if secret_key else os.getenv("UNSPLASH_SECRET_KEY")
        if not self.app_id or not self.access_key or not self.secret_key:
            raise Exception("Unsplash ACCESS_KEY or APP_ID or SECRET_KEY not defined")

    def search(
        self,
        query: str,
        *,
        per_page: int = 5,
        output_type="short",
        orientation="landscape",
    ):
        url = f"https://api.unsplash.com/search/photos"
        response = requests.get(
            url,
            params={"query": query, "per_page": per_page, "orientation": orientation},
            headers={"Authorization": f"Client-ID {self.access_key}"},
        )
        response.raise_for_status()
        photos = response.json()
        if not output_type == "short":
            return photos
        out = [
            {"url": p["urls"]["regular"], "alt": p["alt_description"]}
            for p in photos["results"]
        ]
        return out


class VecteezyImage:
    """
    Wrapper of Vecteezy API

    documentation: https://www.vecteezy.com/api-docs/index.html
    """

    def __init__(self, *, account_id: str = "", api_key: str = ""):
        self.account_id = account_id if account_id else os.getenv("VECTEEZY_ACCOUNT_ID")
        self.api_key = api_key if api_key else os.getenv("VECTEEZY_API_KEY")
        if not self.account_id or not self.api_key:
            raise Exception("Vecteezy API_KEY or ACCOUNT_ID not defined")

    def search(
        self,
        query: str,
        *,
        per_page: int = 5,
        output_type="short",
        orientation="landscape",
    ):
        url = f"https://api.vecteezy.com/v2/{self.account_id}/resources"
        response = requests.get(
            url,
            params={
                "term": query,
                "per_page": per_page,
                "content_type": "photo",
                "orientation": orientation,
            },
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()

        photos = response.json()
        if not output_type == "short":
            return photos
        out = [
            {"url": p["thumbnail_url"], "alt": p["title"]} for p in photos["resources"]
        ]
        return out


class PexelsImage:
    """
    Wrapper of Pexels API

    documentation: https://www.pexels.com/api/documentation
    """

    def __init__(self, api_key: str = ""):
        self.api_key = api_key if api_key else os.getenv("PEXELS_API_KEY")
        if not self.api_key:
            raise RuntimeError("Not PEXELS_API_KEY defined")

    def search(
        self,
        query: str,
        *,
        per_page: int = 5,
        output_type="short",
        orientation="landscape",
    ):
        url = "https://api.pexels.com/v1/search"
        response = requests.get(
            url,
            params={"query": query, "per_page": per_page, "orientation": orientation},
            headers={"Authorization": self.api_key},
        )
        response.raise_for_status()

        photos = response.json()
        if not output_type == "short":
            return photos
        out = [{"url": p["src"]["original"], "alt": p["alt"]} for p in photos["photos"]]
        return out
