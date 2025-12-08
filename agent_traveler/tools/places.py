"""
Tool research about places to get its latitude, longitude (and more) using
the Google Places (new) API
"""

from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext
from agent_traveler.libs.maps import create_kml

from .artifact import save_kml_tool
from agent_traveler.libs.extract_update_data import extract_places_destination


async def research_destination_callback(callback_context: CallbackContext):
    """Update infomartion of researched destinations

    Args:
      callback_context: google ADK callback context

    Returns:
      None
    """
    destinations = callback_context.state.get("destination_data", {}).get(
        "destination_data", []
    )
    places = await extract_places_destination(destinations)
    callback_context.state["places_data"].extend(places)

    return None


async def create_map_points(tool_context: ToolContext):
    """
    Create a file of type KML with the places, to be imported to Google My Maps.
    The output will be saved at a persistent storage.

    Args:
        tool_context: The ADK tool context.

    Returns:
        The status of the operation, with data
    """
    places = tool_context.state["places_data"]

    places = [p for p in places if p.get("lat") and p.get("long")]
    if len(places) > 0:
        output = create_kml(places)
        await save_kml_tool(output, tool_context)
        return {"status": "success", "message": "create KML file", "kml": output}

    return {"status": "error", "message": "No data to create map place"}
