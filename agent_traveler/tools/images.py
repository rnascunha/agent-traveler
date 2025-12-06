"""
Tool to search images from text. Connects to different stock images database.
"""

from agent_traveler.libs.images import PexelsImage


def search_images_tool(query: str):
    """
    Search image based on the 'query' term.

    Args:
        query: term to be searched

    Return:
        Object with status of operation and link to the image.
        If success, returns:
        {
          "status": "success",
          "image": image link,
          "image_description": description of the image
        }
        If fail, returns:
        {
          "status": "error",
          "message": message explaining the error
        }
    """

    try:
        images_search = PexelsImage()
        # images_search = UnsplashImage()
        images = images_search.search(query, per_page=1)
        image = images["photos"][0]
        return {
            "status": "success",
            "image": image["url"],
            "image_description": image.get("alt", ""),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
