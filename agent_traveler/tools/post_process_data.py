from google.adk.agents.callback_context import CallbackContext
from agent_traveler.libs.extract_update_data import improve_extracted_data
from agent_traveler.libs.merge_destinatination_places import merge_data


async def extract_data_callback(callback_context: CallbackContext):
    """
    Get data extracted and improve it

    Args:
      callback_context: google ADK callback context

    Returns:
      None
    """
    extract_data = callback_context.state.get("extracted_data")
    data, places = await improve_extracted_data(extract_data)
    callback_context.state["extracted_data"] = data
    callback_context.state["places_data"] = places

    return None


def merge_destination_place_callback(callback_context: CallbackContext):
    """
    Merge data from "places" to destinations/highlights to improve reports
    Args:
      callback_context: google ADK callback context

    Returns:
      None
    """
    destinations = merge_data(callback_context.state)
    callback_context.state["destinations"] = destinations

    return None
